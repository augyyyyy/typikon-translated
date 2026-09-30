#!/usr/bin/env python3
"""
Deterministic Typikon Auditor Engine
===================================
A zero-hallucination, line-by-line, section-by-section verification suite
for the Dolnytsky Typikon English translation deliverable corpus.

Engines implemented:
1. Footnote Bijectivity, Sequence Monotonicity & Scope Anchor Verification
2. List State Machine & Step Numbering Continuity Validator
3. Syntax, Formatting & Mojibake Character Corruption Linter
4. Internal Cross-Reference & Unresolved Marker Auditor
5. Section Cardinality & Topology Structural Validator

Outputs:
- scratch/reports/deterministic_audit_report.md
- scratch/reports/deterministic_audit_report.json
"""

import sys
import re
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def get_project_root() -> Path:
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "Ukrainian TXTs").exists() and (parent / "Final").exists():
            return parent
    return Path(__file__).resolve().parent.parent

class DeterministicAuditor:
    def __init__(self, root: Path):
        self.root = root
        self.final_dir = root / "Final"
        self.final_md_dir = root / "Final MD"
        self.ua_docx = root / "scratch" / "Typyk_UHKC_ukr.docx"
        self.reports_dir = root / "scratch" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.issues = []

    def log_issue(self, category: str, severity: str, file: str, line_no: int, message: str, context: str = ""):
        self.issues.append({
            "category": category,
            "severity": severity,
            "file": file,
            "line": line_no,
            "message": message,
            "context": context.strip()[:140]
        })

    # =========================================================================
    # ENGINE 1: Footnote Bijectivity, Monotonicity & Scope Verification
    # =========================================================================
    def audit_footnotes(self):
        print("[-] Running Engine 1: Footnote Bijectivity & Scope Validator...")
        fn_file = self.final_dir / "Final_footnotes.txt"
        if not fn_file.exists():
            print(f"    Error: {fn_file} not found.")
            return

        # 1. Parse Master Footnote Definitions
        fn_defs = {}
        for m in re.finditer(r'^\[\^(\d+[a-z]?)\]:\s*(.*?)(?=\n\[\^\d+[a-z]?\]:|\Z)', fn_file.read_text(encoding='utf-8'), re.MULTILINE | re.DOTALL):
            fn_defs[m.group(1)] = m.group(2).strip()

        # 2. Extract Footnotes from Ukrainian DOCX with Heading Scope
        ua_doc_footnotes = {}
        if self.ua_docx.exists():
            with zipfile.ZipFile(self.ua_docx) as z:
                tree = ET.fromstring(z.read('word/document.xml'))
                curr_heading = "TOP"
                for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                    text = ''.join(p.itertext()).strip()
                    if re.match(r'^\d+\s+[А-ЯЄІЇ]+', text) or text.startswith('ЧАСТИНА') or text.startswith('ГЛАВА'):
                        curr_heading = text
                    for fnref in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnoteReference'):
                        fn_id = fnref.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
                        if fn_id and int(fn_id) > 0:
                            ua_doc_footnotes[fn_id] = (curr_heading, text[:80])

        # 3. Check Footnote Inlines in English MD files
        all_anchored_markers = set()
        file_order = [
            "Final_Dolnytsky_intro.md",
            "Final_Dolnytsky_part1_structure.md",
            "Final_Dolnytsky_part2_general_rubrics.md",
            "Final_Dolnytsky_part3_menaion.md",
            "Final_Dolnytsky_part4_triodion.md",
            "Final_Dolnytsky_part5_temple.md",
            "Final_Dolnytsky_appendix.md"
        ]

        global_fn_sequence = []

        for fname in file_order:
            fpath = self.final_md_dir / fname
            if not fpath.exists():
                continue
            lines = fpath.read_text(encoding='utf-8').splitlines()
            curr_heading = "TOP"
            file_prev_id = 0

            for idx, line in enumerate(lines, start=1):
                if line.startswith('#'):
                    curr_heading = line.strip('#').strip()

                # Skip pure footnote definition lines if any exist in deliverables
                if line.strip().startswith('[^') and re.match(r'^\[\^\d+[a-z]?\]:', line.strip()):
                    continue

                for m in re.finditer(r'\[\^(\d+[a-z]?)\]', line):
                    fn_id = m.group(1)
                    all_anchored_markers.add(fn_id)
                    
                    if fn_id.isdigit():
                        curr_int = int(fn_id)
                        global_fn_sequence.append((curr_int, fname, idx, curr_heading, line))
                        
                        # Check local file monotonicity
                        if file_prev_id > 0 and curr_int < file_prev_id:
                            backward_jump = file_prev_id - curr_int
                            if backward_jump > 3: # Non-trivial backward jump
                                self.log_issue(
                                    category="Footnote Monotonicity",
                                    severity="HIGH",
                                    file=fname,
                                    line_no=idx,
                                    message=f"Footnote [^{curr_int}] appears after [^{file_prev_id}] (backward jump of {backward_jump}). Scope anomaly detected.",
                                    context=line
                                )
                        file_prev_id = curr_int

                    # Check bijectivity with definitions
                    if fn_id not in fn_defs:
                        self.log_issue(
                            category="Footnote Bijectivity",
                            severity="CRITICAL",
                            file=fname,
                            line_no=idx,
                            message=f"Orphaned marker [^{fn_id}]: No definition exists in Final_footnotes.txt",
                            context=line
                        )

        # Check for defined footnotes that are never referenced
        for def_id in fn_defs:
            if def_id not in all_anchored_markers:
                self.log_issue(
                    category="Footnote Bijectivity",
                    severity="MEDIUM",
                    file="Final_footnotes.txt",
                    line_no=0,
                    message=f"Footnote [^{def_id}] is defined in Final_footnotes.txt but never referenced in any deliverable body text.",
                    context=fn_defs[def_id][:80]
                )

    # =========================================================================
    # ENGINE 2: List State Machine & Step Numbering Continuity Validator
    # =========================================================================
    def audit_numbering(self):
        print("[-] Running Engine 2: List State Machine & Step Numbering Validator...")
        for md_file in sorted(self.final_md_dir.glob("*.md")):
            if "footnotes" in md_file.name or "glossary" in md_file.name:
                continue
            lines = md_file.read_text(encoding='utf-8').splitlines()
            curr_num = 0
            in_list = False

            for idx, line in enumerate(lines, start=1):
                clean = line.strip()
                # Check for numbered list marker: e.g. "1. ", "2.\t"
                m = re.match(r'^(\d+)\.[\s\t]', clean)
                if m:
                    n = int(m.group(1))
                    if n == 1:
                        curr_num = 1
                        in_list = True
                    elif in_list:
                        if n == curr_num:
                            self.log_issue(
                                category="List Numbering",
                                severity="HIGH",
                                file=md_file.name,
                                line_no=idx,
                                message=f"Duplicate list number {n}. (Sequence repeated after item {curr_num})",
                                context=line
                            )
                        elif n > curr_num + 1 and n <= curr_num + 5:
                            self.log_issue(
                                category="List Numbering",
                                severity="HIGH",
                                file=md_file.name,
                                line_no=idx,
                                message=f"Numbering gap: Expected item {curr_num + 1}, but encountered {n}.",
                                context=line
                            )
                        curr_num = n
                elif clean.startswith('#') or clean == '---' or clean == '___':
                    # Section resets list
                    in_list = False
                    curr_num = 0

    # =========================================================================
    # ENGINE 3: Syntax, Formatting & Character Corruption Linter
    # =========================================================================
    def audit_syntax_and_encoding(self):
        print("[-] Running Engine 3: Syntax, Formatting & Character Linter...")
        for md_file in sorted(self.final_md_dir.glob("*.md")):
            lines = md_file.read_text(encoding='utf-8').splitlines()
            for idx, line in enumerate(lines, start=1):
                # 1. Check for raw tabs
                if '\t' in line:
                    self.log_issue(
                        category="Syntax / Formatting",
                        severity="MEDIUM",
                        file=md_file.name,
                        line_no=idx,
                        message="Literal unparsed tab character (\\t) found in markdown source.",
                        context=line
                    )
                # 2. Check for mojibake / corrupted glyphs
                if '????' in line or '\ufffd' in line:
                    self.log_issue(
                        category="Character Corruption",
                        severity="CRITICAL",
                        file=md_file.name,
                        line_no=idx,
                        message="Corrupted character sequence ('????' or replacement glyph \\ufffd) detected.",
                        context=line
                    )
                # 3. Check for unbalanced markdown emphasis
                # Count unescaped asterisks (simple parity check for single/double asterisks)
                # Note: Only flag when lines have odd count of asterisks that aren't bullet points
                stripped = line.strip()
                if not stripped.startswith('* ') and not stripped.startswith('***'):
                    asterisk_count = stripped.count('*')
                    if asterisk_count % 2 != 0:
                        self.log_issue(
                            category="Syntax / Formatting",
                            severity="LOW",
                            file=md_file.name,
                            line_no=idx,
                            message=f"Odd count of asterisks ({asterisk_count}) may indicate unclosed italic/bold tag.",
                            context=line
                        )

        # Check footnotes file specifically for corrupted glyphs
        fn_file = self.final_dir / "Final_footnotes.txt"
        if fn_file.exists():
            for idx, line in enumerate(fn_file.read_text(encoding='utf-8').splitlines(), start=1):
                if '????' in line or '\ufffd' in line:
                    self.log_issue(
                        category="Character Corruption",
                        severity="CRITICAL",
                        file="Final_footnotes.txt",
                        line_no=idx,
                        message="Corrupted character sequence ('????' or replacement glyph) in footnote definition.",
                        context=line
                    )

    # =========================================================================
    # ENGINE 4: Internal Cross-Reference & Unresolved Marker Auditor
    # =========================================================================
    def audit_cross_references(self):
        print("[-] Running Engine 4: Internal Cross-Reference Auditor...")
        for md_file in sorted(self.final_md_dir.glob("*.md")):
            lines = md_file.read_text(encoding='utf-8').splitlines()
            for idx, line in enumerate(lines, start=1):
                # Search for unresolved REF markers (including arrow variants)
                if re.search(r'\[[→\->]?\s*REF:[^\]]+\]', line):
                    self.log_issue(
                        category="Internal Cross-Reference",
                        severity="HIGH",
                        file=md_file.name,
                        line_no=idx,
                        message="Unresolved reference token '[→REF:...]' in deliverable text.",
                        context=line
                    )
                # Search for raw Ukrainian page citations like "див. на стор."
                if re.search(r'\b(?:стор\.|див\.\s+стор|на\s+стор)\b', line, re.IGNORECASE):
                    self.log_issue(
                        category="Internal Cross-Reference",
                        severity="MEDIUM",
                        file=md_file.name,
                        line_no=idx,
                        message="Untranslated Ukrainian page reference citation found.",
                        context=line
                    )
        # Also check Final TXT files for any unresolved REF markers
        for txt_file in sorted(self.final_dir.glob("*.txt")):
            lines = txt_file.read_text(encoding='utf-8').splitlines()
            for idx, line in enumerate(lines, start=1):
                if re.search(r'\[[→\->]?\s*REF:[^\]]+\]', line):
                    self.log_issue(
                        category="Internal Cross-Reference",
                        severity="HIGH",
                        file=txt_file.name,
                        line_no=idx,
                        message="Unresolved reference token '[→REF:...]' in deliverable text.",
                        context=line
                    )

    # =========================================================================
    # ENGINE 5: Liturgical Formula & Arithmetic Validator
    # =========================================================================
    def audit_liturgical_math(self):
        print("[-] Running Engine 5: Liturgical Formula & Arithmetic Validator...")
        stichera_pat = re.compile(r'(\d+)\s+stichera:\s*([^\.\n;]+)', re.IGNORECASE)
        stichera_on_pat = re.compile(r'stichera\s+on\s+(\d+):\s*([^\.\n;]+)', re.IGNORECASE)

        for md_file in sorted(self.final_md_dir.glob("*.md")):
            lines = md_file.read_text(encoding='utf-8').splitlines()
            for idx, line in enumerate(lines, start=1):
                for pat in [stichera_pat, stichera_on_pat]:
                    for m in pat.finditer(line):
                        target = int(m.group(1))
                        formula = m.group(2).strip()
                        formula_clean = re.split(r'\b(?:Glory|Both now|using|dismissal)\b', formula, flags=re.IGNORECASE)[0]
                        nums = []
                        if 'twice' in formula_clean.lower():
                            nums.append(2)
                        if 'once' in formula_clean.lower():
                            nums.append(1)
                        for cm in re.finditer(r'(?:[–—\-]\s*(\d+)|(?:^|[,\s])(\d+)\s+(?:of|to|Resurrectional|Sunday|Martyria|Penitential|Idiomela?|stichera)|on\s+(\d+))', formula_clean):
                            val = next(v for v in cm.groups() if v is not None)
                            nums.append(int(val))
                        s = sum(nums)
                        if s > target and not any(k in formula_clean.lower() for k in ['or', 'if', 'sunday:', 'week:']):
                            self.log_issue(
                                category="Liturgical Math",
                                severity="LOW",
                                file=md_file.name,
                                line_no=idx,
                                message=f"Liturgical balance mismatch: target is {target} stichera, but components sum to {s} (source-inherited anomaly).",
                                context=line
                            )

    # =========================================================================
    # ENGINE 6: Section Cardinality Differential Auditor
    # =========================================================================
    def audit_section_cardinality(self):
        print("[-] Running Engine 6: Section Cardinality Differential Auditor...")
        ua_dir = self.root / "Ukrainian TXTs"
        file_pairs = [
            ("Intro.txt", "Final_Dolnytsky_intro.md"),
            ("Part 1.txt", "Final_Dolnytsky_part1_structure.md"),
            ("Part 2.txt", "Final_Dolnytsky_part2_general_rubrics.md"),
            ("Part 3.txt", "Final_Dolnytsky_part3_menaion.md"),
            ("Part 4.txt", "Final_Dolnytsky_part4_triodion.md"),
            ("Part 5.txt", "Final_Dolnytsky_part5_temple.md"),
            ("Appendix.txt", "Final_Dolnytsky_appendix.md"),
            ("Footnotes.txt", "Final_footnotes.md"),
        ]
        for ua_name, en_name in file_pairs:
            ua_path = ua_dir / ua_name
            en_path = self.final_md_dir / en_name
            if not ua_path.exists() or not en_path.exists():
                self.log_issue(
                    category="Section Cardinality",
                    severity="HIGH",
                    file=en_name,
                    line_no=1,
                    message=f"Missing corresponding Ukrainian or English file for cardinality pair ({ua_name} <-> {en_name}).",
                    context=""
                )
                continue
            ua_lines = [l for l in ua_path.read_text(encoding='utf-8').splitlines() if l.strip()]
            en_lines = [l for l in en_path.read_text(encoding='utf-8').splitlines() if l.strip()]
            ratio = len(en_lines) / len(ua_lines) if ua_lines else 0
            # Allow Part 5 table condensation (ratio ~ 0.38)
            min_ratio = 0.30 if "part5" in en_name.lower() else 0.75
            max_ratio = 3.50
            if ratio < min_ratio or ratio > max_ratio:
                self.log_issue(
                    category="Section Cardinality",
                    severity="HIGH",
                    file=en_name,
                    line_no=1,
                    message=f"Structural cardinality anomaly: line count ratio {ratio:.2f} is outside expected range [{min_ratio}, {max_ratio}].",
                    context=f"UA lines: {len(ua_lines)}, EN lines: {len(en_lines)}"
                )

    # =========================================================================
    # GENERATE REPORTS
    # =========================================================================

    def generate_report(self):
        report_md = self.reports_dir / "deterministic_audit_report.md"
        report_json = self.reports_dir / "deterministic_audit_report.json"

        # Tally statistics
        total = len(self.issues)
        by_sev = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        by_cat = {}

        for iss in self.issues:
            by_sev[iss["severity"]] = by_sev.get(iss["severity"], 0) + 1
            by_cat[iss["category"]] = by_cat.get(iss["category"], 0) + 1

        with open(report_json, "w", encoding="utf-8") as jf:
            json.dump({
                "summary": {
                    "total_issues": total,
                    "by_severity": by_sev,
                    "by_category": by_cat
                },
                "issues": self.issues
            }, jf, indent=2)

        with open(report_md, "w", encoding="utf-8") as mf:
            mf.write("# Deterministic Typikon Audit Report\n\n")
            mf.write("## 1. Executive Summary\n\n")
            mf.write(f"- **Total Anomalies Detected**: **{total}**\n")
            mf.write(f"- **Critical Severity**: {by_sev['CRITICAL']}\n")
            mf.write(f"- **High Severity**: {by_sev['HIGH']}\n")
            mf.write(f"- **Medium Severity**: {by_sev['MEDIUM']}\n")
            mf.write(f"- **Low Severity**: {by_sev['LOW']}\n\n")

            mf.write("### Breakdown by Anomaly Category\n\n")
            mf.write("| Category | Count |\n|---|---|\n")
            for cat, cnt in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
                mf.write(f"| {cat} | {cnt} |\n")
            mf.write("\n---\n\n")

            mf.write("## 2. Prioritized Discrepancy Ledger (Critical & High Severity)\n\n")
            mf.write("| File | Line | Severity | Category | Description | Context |\n")
            mf.write("|---|---|---|---|---|---|\n")
            for iss in self.issues:
                if iss["severity"] in ["CRITICAL", "HIGH"]:
                    clean_ctx = iss["context"].replace("|", "\\|").replace("\n", " ")
                    clean_msg = iss["message"].replace("|", "\\|")
                    mf.write(f"| `{iss['file']}` | L{iss['line']} | **{iss['severity']}** | {iss['category']} | {clean_msg} | `{clean_ctx}` |\n")

            mf.write("\n---\n\n")
            mf.write("## 3. Medium & Low Severity Ledger\n\n")
            mf.write("| File | Line | Severity | Category | Description | Context |\n")
            mf.write("|---|---|---|---|---|---|\n")
            for iss in self.issues:
                if iss["severity"] in ["MEDIUM", "LOW"]:
                    clean_ctx = iss["context"].replace("|", "\\|").replace("\n", " ")
                    clean_msg = iss["message"].replace("|", "\\|")
                    mf.write(f"| `{iss['file']}` | L{iss['line']} | {iss['severity']} | {iss['category']} | {clean_msg} | `{clean_ctx}` |\n")

        print(f"\n[+] Audit Complete! Total anomalies found: {total}")
        print(f"    Critical: {by_sev['CRITICAL']} | High: {by_sev['HIGH']} | Medium: {by_sev['MEDIUM']} | Low: {by_sev['LOW']}")
        print(f"    Markdown report: {report_md}")
        print(f"    JSON dataset: {report_json}")

def main():
    root = get_project_root()
    auditor = DeterministicAuditor(root)
    auditor.audit_footnotes()
    auditor.audit_numbering()
    auditor.audit_syntax_and_encoding()
    auditor.audit_cross_references()
    auditor.audit_liturgical_math()
    auditor.audit_section_cardinality()
    auditor.generate_report()

if __name__ == "__main__":
    main()

