#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Process File Locking & Atomic Persistence Primitives
==========================================================
Provides OS-level cross-process file locks and atomic write/update helpers
so multiple sequestered monument orchestrator chats can execute in parallel
without corrupting shared root files (codex_registry.json, CHRONICLE.md,
ACTIVE_ORCHESTRATOR_STATE.json, scratch/triage_inbox.jsonl, and .git/index).
"""

import os
import sys
import time
import json
import threading
from pathlib import Path
from typing import Any, Callable, Dict, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
LOCKS_DIR = PROJECT_ROOT / "scratch" / ".locks"
DEFAULT_REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"


class FileLock:
    """
    Cross-process file lock backed by OS-level byte locking (msvcrt on Windows,
    fcntl on POSIX) in scratch/.locks/<lock_name>.lock.
    """

    def __init__(self, lock_name: str, timeout: float = 30.0, poll_interval: float = 0.05) -> None:
        safe_name = "".join(c if (c.isalnum() or c in ("_", "-")) else "_" for c in lock_name)
        self.lock_path = LOCKS_DIR / f"{safe_name}.lock"
        self.timeout = timeout
        self.poll_interval = poll_interval
        self._fd: Optional[int] = None

    def acquire(self) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_RDWR)
                try:
                    if os.name == "nt":
                        import msvcrt
                        os.lseek(fd, 0, os.SEEK_SET)
                        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self._fd = fd
                    return
                except OSError:
                    os.close(fd)
                    raise
            except OSError as exc:
                if time.monotonic() >= deadline:
                    raise TimeoutError(
                        f"Timed out waiting {self.timeout}s for cross-process lock '{self.lock_path.name}'"
                    ) from exc
                time.sleep(self.poll_interval)

    def release(self) -> None:
        if self._fd is None:
            return
        fd = self._fd
        self._fd = None
        try:
            if os.name == "nt":
                import msvcrt
                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_UN)
        except OSError:
            pass
        finally:
            try:
                os.close(fd)
            except OSError:
                pass

    def __enter__(self) -> "FileLock":
        self.acquire()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.release()


def _replace_with_ntfs_retry(tmp_path: Path, target_path: Path, max_retries: int = 20) -> None:
    """
    Atomically replaces target_path with tmp_path, retrying briefly on Windows
    PermissionError when a concurrent process has target_path open for reading.
    """
    for attempt in range(max_retries):
        try:
            os.replace(str(tmp_path), str(target_path))
            return
        except PermissionError:
            if attempt == max_retries - 1:
                try:
                    tmp_path.unlink(missing_ok=True)
                except OSError:
                    pass
                raise
            time.sleep(0.025 * (attempt + 1))


def atomic_write_text(
    path: Path,
    content: str,
    lock_name: Optional[str] = None,
    preserve_crlf: bool = False,
) -> None:
    """
    Writes text to a sibling temporary file and atomically replaces `path`.
    Optionally acquires `FileLock(lock_name)` around the write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    pid = os.getpid()
    tid = threading.get_ident()
    tmp_path = path.parent / f".{path.name}.{pid}.{tid}.tmp"

    def _do_write() -> None:
        use_crlf = preserve_crlf
        if preserve_crlf and path.exists():
            try:
                raw_existing = path.read_bytes()
                use_crlf = b"\r\n" in raw_existing
            except OSError:
                use_crlf = False
        normalized = content.replace("\r\n", "\n")
        if use_crlf:
            normalized = normalized.replace("\n", "\r\n")
        tmp_path.write_bytes(normalized.encode("utf-8"))
        _replace_with_ntfs_retry(tmp_path, path)

    if lock_name:
        with FileLock(lock_name):
            _do_write()
    else:
        _do_write()


def atomic_write_json(
    path: Path,
    data: Dict[str, Any],
    lock_name: Optional[str] = None,
    preserve_crlf: bool = False,
) -> None:
    """
    Serializes `data` as formatted UTF-8 JSON and atomically replaces `path`.
    """
    dumped = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    atomic_write_text(path, dumped, lock_name=lock_name, preserve_crlf=preserve_crlf)


def atomic_append_jsonl(
    path: Path,
    entry: Dict[str, Any],
    lock_name: str = "triage_inbox",
) -> None:
    """
    Appends a single JSONL record to `path` under an exclusive cross-process lock.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    with FileLock(lock_name):
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)
            f.flush()


def atomic_update_registry(
    mutator_fn: Callable[[Dict[str, Any]], Any],
    registry_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Acquires FileLock('codex_registry'), reads the latest codex_registry.json from disk,
    invokes `mutator_fn(registry)` in-place, atomically writes the updated registry back
    (preserving CRLF if present), and returns the updated registry dict.
    """
    target_path = registry_path or DEFAULT_REGISTRY_FILE
    with FileLock("codex_registry"):
        if not target_path.exists():
            raise FileNotFoundError(f"Codex registry not found at: {target_path}")
        raw_bytes = target_path.read_bytes()
        has_crlf = b"\r\n" in raw_bytes
        registry: Dict[str, Any] = json.loads(raw_bytes.decode("utf-8-sig"))
        mutator_fn(registry)
        dumped = json.dumps(registry, indent=2, ensure_ascii=False) + "\n"
        if has_crlf:
            dumped = dumped.replace("\n", "\r\n")
        pid = os.getpid()
        tid = threading.get_ident()
        tmp_path = target_path.parent / f".{target_path.name}.{pid}.{tid}.tmp"
        tmp_path.write_bytes(dumped.encode("utf-8"))
        _replace_with_ntfs_retry(tmp_path, target_path)
        return registry
