#!/usr/bin/env python3
"""
File: formatter.py
Tool: LLMDataHub Harvester — Markdown Formatter
Version: 1.1.0
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Version History:
  1.0.5 — initial formatter
  1.1.0 — 2026-10-09 — added AWESOME-LISTS.md insertion target with
                       year-section fallback patterns. Dedup now scans
                       the whole file (name + URL), not just the section.
                       main() uses classifier v1.1.0 (skip-list + full-
                       archive dedup) and reports rejected count.
"""

import re
from pathlib import Path
from typing import Dict, List

def safe_string(value) -> str:
    if value is None:
        return ""
    return str(value).strip()

def format_dataset_row(repo: Dict) -> str:
    name = safe_string(repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)
    language = safe_string(repo.get("language", ""))

    if len(description) > 120:
        description = description[:117] + "..."

    return f"| [{name}]({url}) | — | Dataset | {language} | {stars}★ | {description} |"

def format_model_row(repo: Dict) -> str:
    name = safe_string(repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)
    language = safe_string(repo.get("language", ""))

    if len(description) > 120:
        description = description[:117] + "..."

    return f"| [{name}]({url}) | — | LLM | {language} | {stars}★ | {description} |"

def format_paper_row(repo: Dict) -> str:
    name = safe_string(repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)

    if len(description) > 120:
        description = description[:117] + "..."

    return f"| [{name}]({url}) | — | — | [Code]({url}) | — | {description} |"

def format_tool_row(repo: Dict) -> str:
    name = safe_string(repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)
    language = safe_string(repo.get("language", ""))

    if len(description) > 120:
        description = description[:117] + "..."

    return f"| [{name}]({url}) | — | Tool | {language} | {description} |"

def format_awesome_row(repo: Dict) -> str:
    name = safe_string(repo.get("full_name", "") or repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)

    if len(description) > 200:
        description = description[:197] + "..."

    return (
        f"<details>\n"
        f"  <summary><strong>{name}</strong> — {stars} ★</summary>\n\n"
        f"  **Description:** {description}\n\n"
        f"  **Link:** [{url}]({url})\n\n"
        f"  **Added:** (auto-harvest)\n"
        f"</details>\n"
    )

def format_candidates(classified: Dict[str, List[Dict]]) -> Dict[str, List[str]]:
    result = {"dataset": [], "model": [], "paper": [], "tool": []}

    for repo in classified.get("dataset", []):
        result["dataset"].append(format_dataset_row(repo))

    for repo in classified.get("model", []):
        result["model"].append(format_model_row(repo))

    for repo in classified.get("paper", []):
        result["paper"].append(format_paper_row(repo))

    for repo in classified.get("tool", []):
        result["tool"].append(format_tool_row(repo))

    return result

def _row_identifiers(row: str) -> List[str]:
    """Extract every identifier we can use for dedup from a formatted row."""
    identifiers = []
    # Markdown link display text
    for m in re.finditer(r'\[([^\]]+)\]', row):
        text = m.group(1).strip()
        if text and text.lower() not in ("code", "github"):
            identifiers.append(text.lower())
    # GitHub URLs — capture owner/repo
    for m in re.finditer(r'https://github\.com/([^\)\s]+)', row):
        owner_repo = m.group(1).strip().rstrip("/").lower()
        if owner_repo:
            identifiers.append(owner_repo)
    return identifiers

def insert_rows_into_file(filename: str, section_pattern: str, rows: List[str]) -> bool:
    """Insert rows into a file after a matching section header."""
    filepath = Path(filename)
    if not filepath.exists():
        print(f"  ❌ File not found: {filename}")
        return False

    with open(filepath, "r") as f:
        content = f.read()

    # Find the section header
    section_match = re.search(section_pattern, content, re.MULTILINE)
    if not section_match:
        print(f"  ❌ Section not found in {filename}: {section_pattern}")
        return False

    # Whole-file lowercase haystack for dedup
    haystack = content.lower()

    existing_entries = []
    for row in rows:
        identifiers = _row_identifiers(row)
        if identifiers and any(ident in haystack for ident in identifiers):
            display = identifiers[0] if identifiers else "(unknown)"
            print(f"  ⏭️  Skipping duplicate: {display}")
            continue
        existing_entries.append(row)

    if not existing_entries:
        print(f"  ℹ️  No new entries to add to {filename}")
        return True

    # Insert rows after the section header
    insert_pos = section_match.end()
    rows_text = "\n" + "\n".join(existing_entries) + "\n"
    new_content = content[:insert_pos] + rows_text + content[insert_pos:]

    with open(filepath, "w") as f:
        f.write(new_content)

    print(f"  ✅ Added {len(existing_entries)} entries to {filename}")
    return True

def _resolve_pattern(filename: str, preferred: str, fallback: str) -> str:
    """If the preferred section pattern isn't in the file, use the fallback."""
    path = Path(filename)
    if not path.exists():
        return preferred
    with open(path, "r") as f:
        content = f.read()
    if re.search(preferred, content, re.MULTILINE):
        return preferred
    return fallback

def generate_insertion_commands(formatted: Dict[str, List[str]]) -> Dict[str, Dict]:
    """Generate insertion data for each file."""
    result = {}

    if formatted["dataset"]:
        result["DATASETS.md"] = {
            "pattern": _resolve_pattern(
                "DATASETS.md",
                r"### Datasets Released in 2025",
                r"##\s*<div id=\"general_aligment\">.*?</div>",
            ),
            "rows": formatted["dataset"],
        }

    if formatted["model"]:
        result["MODELS.md"] = {
            "pattern": _resolve_pattern(
                "MODELS.md",
                r'### <div id="models-2025">2025</div>',
                r'### <div id="models-2026">2026</div>',
            ),
            "rows": formatted["model"],
        }

    if formatted["paper"]:
        result["PAPERS.md"] = {
            "pattern": _resolve_pattern(
                "PAPERS.md",
                r'### <div id="papers-2025">2025</div>',
                r'### <div id="papers-2026">2026</div>',
            ),
            "rows": formatted["paper"],
        }

    if formatted["tool"]:
        result["TOOLS.md"] = {
            "pattern": _resolve_pattern(
                "TOOLS.md",
                r'### <div id="tools-2025">2025</div>',
                r'### <div id="tools-2026">2026</div>',
            ),
            "rows": formatted["tool"],
        }

    return result

def apply_insertions(insertions: Dict[str, Dict]) -> bool:
    """Apply all insertions to files."""
    success = True
    for filename, data in insertions.items():
        print(f"  📝 Applying changes to {filename}...")
        if not insert_rows_into_file(filename, data["pattern"], data["rows"]):
            success = False
    return success

def main():
    from classifier import (
        classify_candidates,
        filter_candidates,
        load_all_existing_entries,
        load_rejected_candidates,
    )
    from github_scraper import scrape_github

    print("  🔄 Running formatter (v1.1.0)...")

    candidates = scrape_github(min_stars=20, max_results=50, recent_years=3, require_license=False)
    existing = load_all_existing_entries()
    rejected = load_rejected_candidates()
    new_candidates = filter_candidates(candidates, existing, rejected)
    print(f"  🚫 Skip-list: {len(rejected)} entries")
    print(f"  🆕 New candidates after filtering: {len(new_candidates)}")

    classified = classify_candidates(new_candidates)

    formatted = format_candidates(classified)

    print(f"\n  📊 Formatted Rows:")
    for category, rows in formatted.items():
        if rows:
            print(f"\n  ## {category.upper()} ({len(rows)})")
            for row in rows[:5]:
                print(f"    {row}")
            if len(rows) > 5:
                print(f"    ... and {len(rows) - 5} more")

    insertions = generate_insertion_commands(formatted)
    print(f"\n  📝 Insertion Data:")
    for filename, data in insertions.items():
        print(f"    {filename}: {len(data['rows'])} rows")

    # Save insertion data for later use
    commands_path = Path.cwd() / "logs" / "insertion_data.txt"
    commands_path.parent.mkdir(exist_ok=True)
    with open(commands_path, "w") as f:
        for filename, data in insertions.items():
            f.write(f"# {filename}\n")
            f.write(f"# Pattern: {data['pattern']}\n")
            for row in data["rows"]:
                f.write(row + "\n")
            f.write("\n")

    print(f"\n  📄 Insertion data saved to: {commands_path}")

if __name__ == "__main__":
    main()