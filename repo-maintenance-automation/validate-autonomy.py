#!/usr/bin/env python3
"""
File: validate-autonomy.py
Tool: LLMDataHub Vault Validator
Version: 1.1.0
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Scans the LLMDataHub archive pages (DATASETS.md,
         REVISED-DESCRIPTIONS.md, MODELS.md, PAPERS.md, TOOLS.md) for
         structure, link integrity, and HF-free compliance.

Usage:
    python repo-maintenance-automation/validate-autonomy.py
    python repo-maintenance-automation/validate-autonomy.py --fix
    python repo-maintenance-automation/validate-autonomy.py --fix --yes

Version History:
  1.0.2 — initial validator
  1.1.0 — 2026-11-22 — H4: HF-link check no longer returns after the
                       first match; all matches reported (report mode)
                       or fixed one-at-a-time with fresh re-scan after
                       each fix (fix mode). H5: MODELS/PAPERS/TOOLS now
                       actually checked; config driven by doc_types.
"""

import re
import sys
import yaml
import shutil
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.yaml"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def backup_file(filepath):
    backup_dir = SCRIPT_DIR / "logs" / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{filepath.name}.{timestamp}.bak"
    shutil.copy2(filepath, backup_path)
    return backup_path


def confirm_fix(description, before, after, auto_yes=False):
    if auto_yes:
        print(f"  \U0001F4DD {description}")
        print(f"     BEFORE: {before}")
        print(f"     AFTER:  {after}")
        return True
    print(f"\n  \u250c\u2500 FIX PROPOSED \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    print(f"  \u2502 {description}")
    print(f"  \u2502")
    print(f"  \u2502 BEFORE: {before}")
    print(f"  \u2502 AFTER:  {after}")
    print(f"  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
    while True:
        response = input("  Apply? [y]es / [n]o / [s]kip all: ").lower().strip()
        if response in ("y", "yes", ""):
            return True
        elif response in ("n", "no"):
            return False
        elif response in ("s", "skip"):
            return "skip_all"
        print("  Please answer y, n, or s")


HF_PATTERNS = [r"huggingface\.co", r"hf\.co"]


def find_next_hf(content):
    """Return (match, url_or_None) for the first HF reference."""
    for pattern in HF_PATTERNS:
        m = re.search(pattern, content, re.IGNORECASE)
        if m:
            start = max(0, m.start() - 50)
            end = min(len(content), m.end() + 50)
            context = content[start:end]
            um = re.search(r"https?://[^\s\)\]]+", context)
            return m, (um.group(0) if um else None)
    return None, None


def check_hf_links(filepath, fix_mode=False, auto_yes=False):
    """Check for HuggingFace links; flag or fix them.

    v1.1.0 semantics:
      - REPORT mode: every HF reference in the file is reported.
      - FIX mode: fixes applied one at a time; after each fix the
        file is re-read fresh (offsets never go stale). A declined
        fix or a bare mention is recorded, not silently swallowed.
    """
    issues = []
    fixes_applied = 0

    with open(filepath, "r") as f:
        content = f.read()

    probe = re.compile("|".join(HF_PATTERNS), re.IGNORECASE)
    offset = 0
    for mm in probe.finditer(content):
        if fix_mode:
            # Re-read for each candidate: file changed by prior fixes.
            with open(filepath, "r") as f:
                fresh = f.read()
            fm, full_url = find_next_hf(fresh)
            if fm is None:
                break
            if full_url is None:
                start = max(0, fm.start() - 50)
                end = min(len(fresh), fm.end() + 50)
                issues.append(f"HF_MENTION_NO_URL: ...{fresh[start:end]}...")
                break
            desc = f"Remove HF link in {filepath.name}"
            result = confirm_fix(desc, full_url, "(HF-hosted removed)", auto_yes)
            if result == "skip_all":
                break
            if result:
                backup_file(filepath)
                with open(filepath, "w") as f:
                    f.write(fresh.replace(full_url, ""))
                fixes_applied += 1
                print("     \u2705 Fixed: removed HF link")
            else:
                issues.append(f"HF_LINK: {full_url}")
        else:
            cstart = max(0, mm.start() - 50)
            cend = min(len(content), mm.end() + 50)
            ctx = content[cstart:cend]
            um = re.search(r"https?://[^\s\)\]]+", ctx)
            if um:
                issues.append(f"HF_LINK: {um.group(0)}")
            else:
                issues.append(f"HF_MENTION: ...{ctx[:60]}...")

    return issues, fixes_applied


def check_graveyard_marker(content, filepath, fix_mode=False, auto_yes=False):
    """Check that HF-only entries have the graveyard marker."""
    issues = []
    fixes_applied = 0
    config = load_config()
    marker = config["validation"]["graveyard_marker"]

    graveyard_section = re.search(
        r"##\s*<div id=\"huggingface-hosted-datasets\">.*?\n(.*?)(?=\n##|$)",
        content,
        re.DOTALL,
    )
    if graveyard_section:
        section_content = graveyard_section.group(1)
        if marker not in section_content:
            if fix_mode:
                desc = f"Add graveyard marker to {filepath.name}"
                result = confirm_fix(desc, "(no marker)", f"{marker} = HuggingFace-hosted (link omitted)", auto_yes)
                if result == "skip_all":
                    pass
                elif result:
                    backup_file(filepath)
                    with open(filepath, "r") as f:
                        fresh = f.read()
                    gs = re.search(
                        r"##\s*<div id=\"huggingface-hosted-datasets\">.*?\n(.*?)(?=\n##|$)",
                        fresh,
                        re.DOTALL,
                    )
                    if gs:
                        new_content = fresh.replace(
                            gs.group(0),
                            gs.group(0) + f"\n\n{marker} = HuggingFace-hosted (link omitted)\n",
                        )
                        with open(filepath, "w") as f:
                            f.write(new_content)
                        fixes_applied += 1
                        print("     \u2705 Fixed: added graveyard marker")
            else:
                issues.append("MISSING_GRAVEYARD_MARKER: Graveyard section missing marker")
    return issues, fixes_applied


def check_sections(filepath, doc_type, config):
    """Check that required sections exist in the file."""
    issues = []
    rules = config["doc_types"].get(doc_type, {})
    required_sections = rules.get("required_sections", [])
    if not required_sections:
        return issues
    with open(filepath, "r") as f:
        content = f.read()
    for section in required_sections:
        escaped_section = re.escape(section)
        pattern = rf"^#{{1,3}}\s+{escaped_section}"
        if not re.search(pattern, content, re.MULTILINE):
            issues.append(f"MISSING_SECTION: '{section}' section not found")
    return issues


def check_placeholder_consistency(datasets_path, revised_path, config):
    """Check that every entry in DATASETS.md has a matching placeholder."""
    issues = []
    with open(datasets_path, "r") as f:
        datasets_content = f.read()
    with open(revised_path, "r") as f:
        revised_content = f.read()

    overlap_pattern = r"### Potential Overlaps.*?\n.*?\n(.*?)(?=\n##|$)"
    datasets_content = re.sub(overlap_pattern, "", datasets_content, flags=re.DOTALL)

    main_sections = re.search(
        r"##\s*<div id=\"general_aligment\">.*?\n(.*?)(?=\n##\s*<div id=\"huggingface-hosted-datasets\">|$)",
        datasets_content,
        re.DOTALL,
    )
    if main_sections:
        main_content = main_sections.group(1)
        table_rows = re.findall(
            r"^\|\s*\[?([^|\]]+)\]?.*?\|",
            main_content,
            re.MULTILINE,
        )
        skip_patterns = config["validation"].get("skip_placeholder_patterns", [])
        for row in table_rows:
            name = row.strip()
            if not name or name in ["Dataset name", "---"]:
                continue
            if any(re.search(p, name) for p in skip_patterns):
                continue
            if f"**{name}**" not in revised_content and f"**{name} " not in revised_content:
                clean_name = re.sub(r"\s*\(.*?\)\s*$", "", name)
                if clean_name and clean_name != name:
                    if f"**{clean_name}**" not in revised_content:
                        issues.append(f"MISSING_PLACEHOLDER: '{name}' has no entry in REVISED-DESCRIPTIONS.md")
                else:
                    issues.append(f"MISSING_PLACEHOLDER: '{name}' has no entry in REVISED-DESCRIPTIONS.md")
    return issues


def run_validation(fix_mode=False, auto_yes=False):
    config = load_config()
    vault_root = Path.cwd()
    all_issues = []
    total_fixes = 0
    stats = {"files_checked": 0, "issues_found": 0}

    mode_label = "FIX MODE" if fix_mode else "REPORT MODE"
    if auto_yes:
        mode_label = "AUTO-FIX MODE"

    print(f"\n{'='*60}")
    print(f"  \U0001F331 LLMDataHub VAULT HEALTH REPORT \u2014 {mode_label}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Repo: {vault_root}")
    print(f"{'='*60}\n")

    datasets_path = vault_root / "DATASETS.md"
    if datasets_path.exists():
        print("\u2500\u2500 DATASETS.md \u2500\u2500")
        stats["files_checked"] += 1

        file_issues = []
        fixes = 0

        hf_issues, hf_fixes = check_hf_links(datasets_path, fix_mode, auto_yes)
        file_issues.extend(hf_issues)
        fixes += hf_fixes

        with open(datasets_path, "r") as f:
            content = f.read()
        marker_issues, marker_fixes = check_graveyard_marker(content, datasets_path, fix_mode, auto_yes)
        file_issues.extend(marker_issues)
        fixes += marker_fixes

        section_issues = check_sections(datasets_path, "datasets", config)
        file_issues.extend(section_issues)

        if file_issues:
            print("  \u26a0\ufe0f  DATASETS.md")
            for issue in file_issues:
                print(f"     \u2192 {issue}")
                stats["issues_found"] += 1
            all_issues.extend([f"DATASETS.md: {i}" for i in file_issues])
        else:
            print("  \u2705 DATASETS.md \u2014 clean")
        total_fixes += fixes
    else:
        print("  \u274c DATASETS.md not found")
        all_issues.append("MISSING_FILE: DATASETS.md not found")
        stats["issues_found"] += 1

    revised_path = vault_root / "REVISED-DESCRIPTIONS.md"
    if revised_path.exists():
        print("\u2500\u2500 REVISED-DESCRIPTIONS.md \u2500\u2500")
        stats["files_checked"] += 1

        file_issues = check_sections(revised_path, "revised_descriptions", config)

        if file_issues:
            print("  \u26a0\ufe0f  REVISED-DESCRIPTIONS.md")
            for issue in file_issues:
                print(f"     \u2192 {issue}")
                stats["issues_found"] += 1
            all_issues.extend([f"REVISED-DESCRIPTIONS.md: {i}" for i in file_issues])
        else:
            print("  \u2705 REVISED-DESCRIPTIONS.md \u2014 clean")
    else:
        print("  \u274c REVISED-DESCRIPTIONS.md not found")
        all_issues.append("MISSING_FILE: REVISED-DESCRIPTIONS.md not found")
        stats["issues_found"] += 1

    for doc_type, fname in (("models", "MODELS.md"), ("papers", "PAPERS.md"), ("tools", "TOOLS.md")):
        fpath = vault_root / fname
        if not fpath.exists():
            print(f"  \u274c {fname} not found")
            all_issues.append(f"MISSING_FILE: {fname} not found")
            stats["issues_found"] += 1
            continue
        print(f"\u2500\u2500 {fname} \u2500\u2500")
        stats["files_checked"] += 1

        file_issues = check_sections(fpath, doc_type, config)

        if file_issues:
            print(f"  \u26a0\ufe0f  {fname}")
            for issue in file_issues:
                print(f"     \u2192 {issue}")
                stats["issues_found"] += 1
            all_issues.extend([f"{fname}: {i}" for i in file_issues])
        else:
            print(f"  \u2705 {fname} \u2014 clean")

    if datasets_path.exists() and revised_path.exists():
        print("\u2500\u2500 Placeholder Consistency \u2500\u2500")
        placeholder_issues = check_placeholder_consistency(datasets_path, revised_path, config)
        if placeholder_issues:
            for issue in placeholder_issues:
                print(f"  \U0001F4DD {issue}")
                stats["issues_found"] += 1
            all_issues.extend(placeholder_issues)
        else:
            print("  \u2705 All entries have placeholders")

    print(f"\n{'='*60}")
    print(f"  \U0001F4CA SUMMARY")
    print(f"  Files checked: {stats['files_checked']}")
    print(f"  Issues found:  {stats['issues_found']}")
    if fix_mode:
        print(f"  Fixes applied: {total_fixes}")
    if stats["issues_found"] == 0:
        print("  \u2705 Vault is healthy. The mycelium is clean.")
    else:
        if fix_mode:
            print("  \u26a0\ufe0f  Remaining issues require manual attention.")
        else:
            print("  \u26a0\ufe0f  Run with --fix to resolve auto-fixable issues.")
    print(f"{'='*60}\n")

    if config.get("reporting", {}).get("save_report", False):
        log_dir = SCRIPT_DIR / config["reporting"].get("output_dir", "logs/")
        log_dir.mkdir(exist_ok=True)
        report_path = log_dir / config["reporting"].get("report_filename", "vault_health_report.txt")
        with open(report_path, "w") as f:
            f.write(f"LLMDataHub Vault Health Report \u2014 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Mode: {mode_label}\n")
            f.write(f"Repo: {vault_root}\n")
            f.write(f"Files checked: {stats['files_checked']}\n")
            f.write(f"Issues found: {stats['issues_found']}\n")
            if fix_mode:
                f.write(f"Fixes applied: {total_fixes}\n")
            f.write("\n")
            for issue in all_issues:
                f.write(f"{issue}\n")
        print(f"  Report saved to: {report_path}")

    return 0 if stats["issues_found"] == 0 else 1


if __name__ == "__main__":
    fix_mode = "--fix" in sys.argv
    auto_yes = "--yes" in sys.argv
    sys.exit(run_validation(fix_mode=fix_mode, auto_yes=auto_yes))
