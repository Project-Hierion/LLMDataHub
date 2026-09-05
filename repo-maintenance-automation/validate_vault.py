#!/usr/bin/env python3
"""
File: validate_vault.py
Tool: LLMDataHub Vault Validator
Version: 1.0.2
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Scans LLMDataHub repo and validates DATASETS.md and
         REVISED-DESCRIPTIONS.md for structure, link integrity,
         and HF-free compliance.

Usage:
    python repo-maintenance-automation/validate_vault.py
    python repo-maintenance-automation/validate_vault.py --fix
    python repo-maintenance-automation/validate_vault.py --fix --yes
"""

import os
import re
import sys
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

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
        print(f"  📝 {description}")
        print(f"     BEFORE: {before}")
        print(f"     AFTER:  {after}")
        return True
    print(f"\n  ┌─ FIX PROPOSED ─────────────────────────────")
    print(f"  │ {description}")
    print(f"  │")
    print(f"  │ BEFORE: {before}")
    print(f"  │ AFTER:  {after}")
    print(f"  └───────────────────────────────────────────")
    while True:
        response = input("  Apply? [y]es / [n]o / [s]kip all: ").lower().strip()
        if response in ("y", "yes", ""):
            return True
        elif response in ("n", "no"):
            return False
        elif response in ("s", "skip"):
            return "skip_all"
        print("  Please answer y, n, or s")

def check_hf_links(content, filepath, fix_mode=False, auto_yes=False):
    """Check for HuggingFace links and flag them."""
    issues = []
    fixes_applied = 0
    forbidden = [
        r"huggingface\.co",
        r"hf\.co",
    ]
    for pattern in forbidden:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end]
            url_match = re.search(r'https?://[^\s\)\]]+', context)
            if url_match:
                full_url = url_match.group(0)
                if fix_mode:
                    desc = f"Remove HF link in {filepath.name}"
                    before = full_url
                    after = "(HF-hosted 🤑)"
                    result = confirm_fix(desc, before, after, auto_yes)
                    if result == "skip_all":
                        auto_yes = False
                    elif result:
                        backup_file(filepath)
                        new_content = content.replace(full_url, "")
                        with open(filepath, "w") as f:
                            f.write(new_content)
                        fixes_applied += 1
                        print(f"     ✅ Fixed: removed HF link")
                        return [], fixes_applied
                else:
                    issues.append(f"HF_LINK: {full_url}")
    return issues, fixes_applied

def check_graveyard_marker(content, filepath, fix_mode=False, auto_yes=False):
    """Check that HF-only entries have the graveyard marker."""
    issues = []
    fixes_applied = 0
    config = load_config()
    marker = config["validation"]["graveyard_marker"]
    
    graveyard_section = re.search(
        r'##\s*<div id="huggingface-hosted-datasets">.*?\n(.*?)(?=\n##|$)',
        content,
        re.DOTALL
    )
    if graveyard_section:
        section_content = graveyard_section.group(1)
        if marker not in section_content:
            if fix_mode:
                desc = f"Add graveyard marker to {filepath.name}"
                before = "(no marker)"
                after = f"{marker} = HuggingFace-hosted (link omitted)"
                result = confirm_fix(desc, before, after, auto_yes)
                if result == "skip_all":
                    auto_yes = False
                elif result:
                    backup_file(filepath)
                    new_content = content.replace(
                        graveyard_section.group(0),
                        graveyard_section.group(0) + f"\n\n{marker} = HuggingFace-hosted (link omitted)\n"
                    )
                    with open(filepath, "w") as f:
                        f.write(new_content)
                    fixes_applied += 1
                    print(f"     ✅ Fixed: added graveyard marker")
                    return [], fixes_applied
            else:
                issues.append("MISSING_GRAVEYARD_MARKER: Graveyard section missing 🤑 marker")
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
    """Check that every entry in DATASETS.md has a matching placeholder in REVISED-DESCRIPTIONS.md."""
    issues = []
    with open(datasets_path, "r") as f:
        datasets_content = f.read()
    with open(revised_path, "r") as f:
        revised_content = f.read()
    
    # Remove the overlap table section entirely from consideration
    overlap_pattern = r'### Potential Overlaps.*?\n.*?\n(.*?)(?=\n##|$)'
    datasets_content = re.sub(overlap_pattern, '', datasets_content, flags=re.DOTALL)
    
    # Extract dataset names from DATASETS.md (open-source sections only, not graveyard)
    main_sections = re.search(
        r'##\s*<div id="general_aligment">.*?\n(.*?)(?=\n##\s*<div id="huggingface-hosted-datasets">|$)',
        datasets_content,
        re.DOTALL
    )
    if main_sections:
        main_content = main_sections.group(1)
        table_rows = re.findall(
            r'^\|\s*\[?([^\|\]]+)\]?.*?\|',
            main_content,
            re.MULTILINE
        )
        skip_patterns = config["validation"].get("skip_placeholder_patterns", [])
        for row in table_rows:
            name = row.strip()
            if not name or name in ["Dataset name", "---"]:
                continue
            if any(re.search(p, name) for p in skip_patterns):
                continue
            if f"**{name}**" not in revised_content and f"**{name} " not in revised_content:
                clean_name = re.sub(r'\s*\(.*?\)\s*$', '', name)
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
    print(f"  🌱 LLMDataHub VAULT HEALTH REPORT — {mode_label}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Repo: {vault_root}")
    print(f"{'='*60}\n")

    # Check DATASETS.md
    datasets_path = vault_root / "DATASETS.md"
    if datasets_path.exists():
        print(f"── DATASETS.md ──")
        stats["files_checked"] += 1
        
        with open(datasets_path, "r") as f:
            content = f.read()
        
        file_issues = []
        fixes = 0
        
        hf_issues, hf_fixes = check_hf_links(content, datasets_path, fix_mode, auto_yes)
        file_issues.extend(hf_issues)
        fixes += hf_fixes
        
        marker_issues, marker_fixes = check_graveyard_marker(content, datasets_path, fix_mode, auto_yes)
        file_issues.extend(marker_issues)
        fixes += marker_fixes
        
        section_issues = check_sections(datasets_path, "datasets", config)
        file_issues.extend(section_issues)
        
        if file_issues:
            print(f"  ⚠️  DATASETS.md")
            for issue in file_issues:
                print(f"     → {issue}")
                stats["issues_found"] += 1
            all_issues.extend([f"DATASETS.md: {i}" for i in file_issues])
        else:
            print(f"  ✅ DATASETS.md — clean")
        total_fixes += fixes
    else:
        print(f"  ❌ DATASETS.md not found")
        all_issues.append("MISSING_FILE: DATASETS.md not found")

    # Check REVISED-DESCRIPTIONS.md
    revised_path = vault_root / "REVISED-DESCRIPTIONS.md"
    if revised_path.exists():
        print(f"── REVISED-DESCRIPTIONS.md ──")
        stats["files_checked"] += 1
        
        with open(revised_path, "r") as f:
            content = f.read()
        
        file_issues = []
        fixes = 0
        
        section_issues = check_sections(revised_path, "revised_descriptions", config)
        file_issues.extend(section_issues)
        
        if file_issues:
            print(f"  ⚠️  REVISED-DESCRIPTIONS.md")
            for issue in file_issues:
                print(f"     → {issue}")
                stats["issues_found"] += 1
            all_issues.extend([f"REVISED-DESCRIPTIONS.md: {i}" for i in file_issues])
        else:
            print(f"  ✅ REVISED-DESCRIPTIONS.md — clean")
        total_fixes += fixes
    else:
        print(f"  ❌ REVISED-DESCRIPTIONS.md not found")
        all_issues.append("MISSING_FILE: REVISED-DESCRIPTIONS.md not found")

    # Check placeholder consistency
    if datasets_path.exists() and revised_path.exists():
        print(f"── Placeholder Consistency ──")
        placeholder_issues = check_placeholder_consistency(datasets_path, revised_path, config)
        if placeholder_issues:
            for issue in placeholder_issues:
                print(f"  📝 {issue}")
                stats["issues_found"] += 1
            all_issues.extend(placeholder_issues)
        else:
            print(f"  ✅ All entries have placeholders")

    print(f"\n{'='*60}")
    print(f"  📊 SUMMARY")
    print(f"  Files checked: {stats['files_checked']}")
    print(f"  Issues found:  {stats['issues_found']}")
    if fix_mode:
        print(f"  Fixes applied: {total_fixes}")
    if stats["issues_found"] == 0:
        print(f"  ✅ Vault is healthy. The mycelium is clean.")
    else:
        if fix_mode:
            print(f"  ⚠️  Remaining issues require manual attention.")
        else:
            print(f"  ⚠️  Run with --fix to resolve auto-fixable issues.")
    print(f"{'='*60}\n")

    if config.get("reporting", {}).get("save_report", False):
        log_dir = SCRIPT_DIR / config["reporting"].get("output_dir", "logs/")
        log_dir.mkdir(exist_ok=True)
        report_path = log_dir / config["reporting"].get("report_filename", "vault_health_report.txt")
        with open(report_path, "w") as f:
            f.write(f"LLMDataHub Vault Health Report — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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
    exit(run_validation(fix_mode=fix_mode, auto_yes=auto_yes))
