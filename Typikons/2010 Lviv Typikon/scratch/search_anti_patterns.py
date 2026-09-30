import argparse
import os
import re
import sys


def detect_bare_except(lines, i, filepath):
    """Return (True, code) if bare except followed by pass or empty block."""
    line = lines[i].rstrip('\n')
    stripped = line.strip()
    # ignore empty or pure comments
    if not stripped or stripped.startswith('#'):
        return False, None

    # Match exactly `except:` or `except Exception:`
    match_except = re.match(r'^\s*except\s*(?::|Exception\s*:)\s*$', stripped)
    if not match_except:
        return False, None

    # Case 1: pass on the same line
    if re.search(r':\s*pass\s*(#.*)?$', stripped):
        return True, stripped

    # Case 2: look at following lines for pass or empty block
    current_indent = len(line) - len(line.lstrip())
    for j in range(i + 1, min(i + 5, len(lines))):
        next_line = lines[j].rstrip('\n')
        next_stripped = next_line.strip()
        if next_stripped == '' or next_stripped.startswith('#'):
            continue
        next_indent = len(next_line) - len(next_line.lstrip())
        if next_stripped == 'pass':
            return True, stripped
        if next_indent <= current_indent:
            # block is empty (dedent or another control keyword)
            return True, stripped
        # some other statement inside the block → not empty
        break
    return False, None


def detect_hardcoded_paths(line):
    r"""Check for hardcoded absolute paths like C:\Users, E:\, OneDrive/Documents."""
    if re.search(r'[A-Za-z]:\\', line):
        return True
    if re.search(r'OneDrive[\\/]Documents', line):
        return True
    return False


def detect_missing_encoding(line):
    """Find open(...) calls without encoding parameter in the same line."""
    if re.search(r'\bopen\s*\(', line) and 'encoding' not in line:
        return True
    return False


def detect_git_no_pager(line):
    """Detect git commands (diff, log, show, blame) without pager disabling."""
    # Look for 'git' followed by one of the commands
    cmd_match = re.search(r'(?:["\'])git\s+(diff|log|show|blame)', line)
    if not cmd_match:
        return False

    # If --no-pager is present anywhere on the line, skip
    if '--no-pager' in line:
        return False
    # If PAGER is explicitly set to 'cat' or empty, skip
    if re.search(r'(?:PAGER\s*=\s*["\']cat["\']|PAGER\s*=)', line):
        return False
    return True


def detect_fragile_regex(line):
    """Detect regex patterns that use word+\d+ for structural headers."""
    # Look for patterns like r'Ode \d+', 'Chapter \d+' etc, inside re.compile/search/match
    if 're.' not in line:
        return False
    if re.search(r'(?:ode|chapter|section|part|heading|titre)\s+\\d\+', line, re.IGNORECASE):
        return True
    return False


def scan_file(filepath):
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        # skip unreadable files
        return findings

    for i, line in enumerate(lines):
        bare, code = detect_bare_except(lines, i, filepath)
        if bare:
            findings.append((filepath, i + 1, 'Bare except (pass/empty)', code))

        if detect_hardcoded_paths(line):
            findings.append((filepath, i + 1, 'Hardcoded absolute path', line.rstrip('\n').strip()))

        if detect_missing_encoding(line):
            findings.append((filepath, i + 1, 'Missing encoding in open()', line.rstrip('\n').strip()))

        if detect_git_no_pager(line):
            findings.append((filepath, i + 1, 'Git command without pager disable', line.rstrip('\n').strip()))

        if detect_fragile_regex(line):
            findings.append((filepath, i + 1, 'Fragile regex for structural headers', line.rstrip('\n').strip()))

    return findings


def main():
    parser = argparse.ArgumentParser(description='Scan directory for anti-patterns.')
    parser.add_argument('directory', nargs='?', default='.',
                        help='Target directory (default: current directory)')
    args = parser.parse_args()
    target_dir = args.directory

    all_findings = []
    for root, dirs, files in os.walk(target_dir):
        for filename in files:
            if not (filename.endswith('.py') or filename.endswith('.md')):
                continue
            full_path = os.path.join(root, filename)
            all_findings.extend(scan_file(full_path))

    if not all_findings:
        print("No anti-patterns found.")
        return

    # Print markdown table
    print("| File | Line | Anti-Pattern | Code |")
    print("| --- | --- | --- | --- |")
    for fname, lineno, pattern, snippet in all_findings:
        # Escape pipe characters in snippet for markdown
        safe_snippet = snippet.replace('|', '\\|')
        # Truncate if too long
        if len(safe_snippet) > 80:
            safe_snippet = safe_snippet[:77] + '...'
        print(f"| {fname} | {lineno} | {pattern} | `{safe_snippet}` |")


if __name__ == '__main__':
    import sys, io
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()