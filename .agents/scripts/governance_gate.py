#!/usr/bin/env python3
"""
Translation Spoke Runtime Pre-Tool Hook Sandbox (governance_gate.py)
====================================================================
Enforces subagent sandbox boundaries at runtime via race-free transcript
header self-identification:
  1. Blocks ephemeral_translator subagents from calling search_web.
  2. Blocks ephemeral_translator subagents from executing external network
     queries or orthographic regex gaming via run_command.
  3. Restricts ephemeral_translator file writes/edits strictly to
     Liturgical Monuments/ (Source Text/, Draft/, Audit_Reports/),
     scratch/, or .gemini/antigravity/brain/.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

NETWORK_CMD_RE = re.compile(
    r"(?:urllib\.request|requests\.(?:get|post)|invoke-webrequest|invoke-restmethod|api\.duckduckgo\.com|curl\s+http)",
    re.IGNORECASE,
)

REGEX_GAMING_CMD_RE = re.compile(
    r"(?:\.replace\(\s*['\"]от['\"]\s*,\s*['\"]ѿ['\"]\)|слава\s+ѿцю|test_replacements)",
    re.IGNORECASE,
)


def get_brain_root() -> Path:
    env_brain = os.environ.get("ANTIGRAVITY_BRAIN_DIR")
    if env_brain:
        return Path(env_brain)
    return Path.home() / ".gemini" / "antigravity" / "brain"


WORKER_DISPATCH_SIGNATURES = (
    "context-sequestered liturgical scribe and translator",
    "execute the work order at:",
    "you are ephemeral_translator",
    "execute work_order_cohort_",
    "targeted flash retry (attempt 1/1) for",
    "delta-only continuation retry (attempt 1/1) for",
)

BOOST_ENVELOPE_RE = re.compile(
    r"<(?:original_task|prior_attempt|instructions)>.*?</(?:original_task|prior_attempt|instructions)>",
    re.IGNORECASE | re.DOTALL,
)


def _strip_boost_envelopes(text: str) -> str:
    if not text:
        return ""
    return BOOST_ENVELOPE_RE.sub("", text)


def is_ephemeral_translator_subagent(conv_id: str, last_user_input: str = "") -> bool:
    if not conv_id or conv_id.startswith("test-parent-"):
        return False
    lui_clean = _strip_boost_envelopes(last_user_input or "").lower()
    if any(sig in lui_clean for sig in WORKER_DISPATCH_SIGNATURES):
        return True
    try:
        log_dir = get_brain_root() / conv_id.strip() / ".system_generated" / "logs"
        for tname in ("transcript_full.jsonl", "transcript.jsonl"):
            tpath = log_dir / tname
            if tpath.exists():
                with open(tpath, "r", encoding="utf-8", errors="ignore") as tf:
                    line0 = tf.readline().strip()
                if not line0:
                    continue
                try:
                    step0 = json.loads(line0)
                    if isinstance(step0, dict):
                        if step0.get("step_index", 0) != 0:
                            continue
                        if str(step0.get("source") or "").upper() == "USER_EXPLICIT":
                            continue
                        content_str = str(step0.get("content") or "")
                        if "<prior_attempt>" in content_str or "<original_task>" in content_str:
                            content_str = _strip_boost_envelopes(content_str)
                        hdr_low = content_str.lower()
                    else:
                        hdr_low = _strip_boost_envelopes(line0).lower()
                except ValueError:
                    hdr_low = _strip_boost_envelopes(line0).lower()
                if '"source":"user_explicit"' not in hdr_low.replace(" ", "") and any(
                    sig in hdr_low for sig in WORKER_DISPATCH_SIGNATURES
                ):
                    return True
    except OSError:
        return False
    return False


def main() -> None:
    try:
        input_data: Dict[str, Any] = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"decision": "allow"}))
        return

    conv_id = str(input_data.get("conversationId") or "")
    last_user_input = str(input_data.get("lastUserInput") or "")
    tool_call = input_data.get("toolCall") or {}
    tool_name = str(tool_call.get("name") or "")
    args = tool_call.get("args") or {}
    if not isinstance(args, dict):
        args = {}

    if is_ephemeral_translator_subagent(conv_id, last_user_input):
        if tool_name == "search_web":
            print(json.dumps({
                "decision": "deny",
                "reason": (
                    "[SUBAGENT SANDBOX VIOLATION — RULE 1 & RULE 16] "
                    "ephemeral_translator subagents are strictly prohibited from calling search_web. "
                    "Translate strictly from the physical 300-DPI facsimile images; mark illegible loci "
                    "with [illegible] or [lacuna] for Phase 2 Argon review."
                ),
            }))
            sys.exit(0)

        if tool_name in ("write_file", "edit_file"):
            t_path = str(args.get("Path") or args.get("TargetFile") or "").replace("\\", "/").lower()
            if t_path.endswith(".py"):
                print(json.dumps({
                    "decision": "deny",
                    "reason": (
                        "[SUBAGENT SANDBOX VIOLATION — SGC-01A] ephemeral_translator subagents are strictly forbidden "
                        "from creating Python generator scripts (.py). Write Markdown/text deliverables directly to "
                        "Source Text/ and Draft/ using write_file."
                    ),
                }))
                sys.exit(0)
            allowed_write = (
                "/source text/" in t_path
                or "/draft/" in t_path
                or "/audit_reports/" in t_path
                or "/scratch/" in t_path
                or "/.gemini/antigravity/brain/" in t_path
            )
            if t_path and not allowed_write:
                print(json.dumps({
                    "decision": "deny",
                    "reason": (
                        f"[SUBAGENT SANDBOX VIOLATION] ephemeral_translator subagents may only write to "
                        f"Source Text/, Draft/, or scratch/. Attempted write to '{t_path}' is strictly prohibited."
                    ),
                }))
                sys.exit(0)

        if tool_name == "run_command":
            cmd_str = str(args.get("CommandLine") or "")
            cmd_low = cmd_str.lower()
            if NETWORK_CMD_RE.search(cmd_str):
                print(json.dumps({
                    "decision": "deny",
                    "reason": (
                        "[SUBAGENT SANDBOX VIOLATION — ZERO EXTERNAL NETWORK LOOKUPS] "
                        "ephemeral_translator subagents are strictly forbidden from executing network/web queries via run_command."
                    ),
                }))
                sys.exit(0)
            if REGEX_GAMING_CMD_RE.search(cmd_str):
                print(json.dumps({
                    "decision": "deny",
                    "reason": (
                        "[SUBAGENT SANDBOX VIOLATION — VECTOR 5C ORTHOGRAPHIC GAMING] "
                        "Programmatic regex replacement of 'от' -> 'ѿ' is strictly forbidden."
                    ),
                }))
                sys.exit(0)
            if any(tok in cmd_low for tok in ("governance_gate.py", "run_small_pause_gate.py", "autonomous_orchestrator.py", "git_index.lock")):
                print(json.dumps({
                    "decision": "deny",
                    "reason": (
                        "[SUBAGENT SANDBOX VIOLATION] "
                        "ephemeral_translator subagents are strictly forbidden from executing or modifying engine gate scripts or lock files."
                    ),
                }))
                sys.exit(0)

    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
