#!/usr/bin/env python3
"""
File: harvest.py
Tool: LLMDataHub Harvester — Main Orchestrator
Version: 1.2.0
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Version History:
  1.0.4 — initial orchestrator
  1.1.0 — 2026-10-09 — persistent skip-list and full-archive dedup
  1.1.1 — 2026-10-09 — all log/script paths consolidated to
                       repo-maintenance-automation/logs/
  1.2.0 — 2026-10-17 — structured logging with run-ID correlation;
                       PR body written BEFORE any risky operations so
                       it always exists for create-pull-request and
                       artifact upload even if insertion fails.
"""

import sys
import time
import os
from pathlib import Path
from typing import List, Dict

from logger import get_logger

from github_scraper import scrape_github
from classifier import (
    classify_candidates,
    filter_candidates,
    load_all_existing_entries,
    load_rejected_candidates,
)
from formatter import format_candidates, generate_insertion_commands, apply_insertions

SCRIPT_DIR = Path(__file__).resolve().parent
LOGS_DIR = SCRIPT_DIR / "logs"

log = get_logger("harvest")

def print_banner(text: str, char: str = "=", width: int = 60):
    print(f"\n{char * width}")
    print(f"  {text}")
    print(f"{char * width}\n")

def is_pr_mode() -> bool:
    return "--pr" in sys.argv or os.environ.get("GITHUB_ACTIONS") == "true"

def human_review(classified: Dict[str, List[Dict]]) -> bool:
    total = sum(len(repos) for repos in classified.values())

    print_banner("🌱 HARVEST COMPLETE", "=")

    print(f"  📊 Summary:")
    for category, repos in classified.items():
        if repos:
            print(f"     {category}: {len(repos)}")
    print(f"     TOTAL: {total}")

    print(f"\n  📄 Full report: repo-maintenance-automation/logs/classification_report.txt")

    print(f"\n  🔍 Top Candidates:")
    for category, repos in classified.items():
        if repos:
            print(f"\n    [{category.upper()}]")
            for repo in repos[:3]:
                stars = repo.get("stars", 0)
                name = repo.get("full_name", "")
                score = repo.get("_score", 0)
                print(f"      - {name} ({stars}★, score: {score:.2f})")
            if len(repos) > 3:
                print(f"      ... and {len(repos) - 3} more")

    if is_pr_mode():
        log.info("Running in PR mode — auto-approving for PR generation")
        return True

    print("\n" + "-" * 60)
    print("  ❓ Add these to the archive?")
    print("     [y] Yes — format and insert everything")
    print("     [N] No — reject and log")
    print("     [exit] Abort — clean exit")
    print("-" * 60)

    while True:
        response = input("  > ").lower().strip()
        if response in ("y", "yes"):
            return True
        elif response in ("n", "no", ""):
            return False
        elif response in ("exit", "q", "quit"):
            print("  🍄 Aborted by user. No changes made.")
            sys.exit(0)
        else:
            print("  Please enter y, N, or exit")

def generate_pr_body(classified: Dict[str, List[Dict]]) -> str:
    lines = [
        "## 🌱 Weekly Harvest\n",
        "Automated harvest of new open-source LLM resources.\n",
        "### What Was Found\n",
    ]

    for category, repos in classified.items():
        if repos:
            lines.append(f"- **{category.capitalize()}:** {len(repos)}")

    lines.append("\n### Review Instructions")
    lines.append("1. Check the report in `repo-maintenance-automation/logs/classification_report.txt`")
    lines.append("2. Review the proposed additions")
    lines.append("3. **Merge** to approve everything")
    lines.append("4. **Close** to reject everything")
    lines.append("5. **Edit** to cherry-pick specific entries")

    lines.append("\n### Top Candidates\n")
    for category, repos in classified.items():
        if repos:
            lines.append(f"#### {category.upper()}")
            for repo in repos[:5]:
                stars = repo.get("stars", 0)
                name = repo.get("full_name", "")
                desc = repo.get("description", "")[:80] if repo.get("description") else "no description"
                lines.append(f"- [{name}]({repo.get('url', '')}) — {stars}★ — {desc}...")
            if len(repos) > 5:
                lines.append(f"- ... and {len(repos) - 5} more")
            lines.append("")

    lines.append("---")
    lines.append("*Let's keep open-source, open. Together.*")

    return "\n".join(lines)

def main():
    log.info("LLMDataHub Harvester starting")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Scrape
    log.info("Scraping GitHub for candidates...")
    candidates = scrape_github(min_stars=20, max_results=100, recent_years=3, require_license=False)
    log.info(f"Scrape complete: {len(candidates)} candidates")

    # Step 2: Dedupe + skip-list
    log.info("Filtering against archive and skip-list...")
    existing = load_all_existing_entries()
    rejected = load_rejected_candidates()
    new_candidates = filter_candidates(candidates, existing, rejected)
    log.info(f"Existing archive entries: {len(existing)}")
    log.info(f"Rejected candidates on skip-list: {len(rejected)}")
    log.info(f"New candidates after filtering: {len(new_candidates)}")

    # Step 3: Classify
    log.info("Classifying candidates...")
    classified = classify_candidates(new_candidates)

    # Step 4: Save report
    report_path = LOGS_DIR / "classification_report.txt"
    with open(report_path, "w") as f:
        f.write("=== CLASSIFICATION REPORT ===\n\n")
        for category, repos in classified.items():
            if repos:
                f.write(f"\n## {category.upper()} ({len(repos)})\n")
                for repo in repos:
                    f.write(f"- {repo['full_name']} ({repo['stars']}★)\n")
                    f.write(f"  Score: {repo.get('_score', 0):.2f}\n")
                    f.write(f"  URL: {repo['url']}\n")
                    desc = repo.get('description', '') or ''
                    if desc:
                        f.write(f"  Description: {desc[:200]}\n")
                    f.write("\n")

    log.info(f"Report saved to: {report_path}")

    # Step 5: Human review
    if not human_review(classified):
        log.info("Rejected by user. Logging and exiting.")
        log_path = LOGS_DIR / "harvest_rejected.txt"
        with open(log_path, "w") as f:
            f.write(f"Harvest rejected at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for category, repos in classified.items():
                if repos:
                    f.write(f"\n{category.upper()}: {len(repos)}\n")
                    for repo in repos:
                        f.write(f"  - {repo['full_name']}\n")
        log.info(f"Rejection log saved to: {log_path}")
        sys.exit(0)

    # Step 6: Format and apply changes
    log.info("Formatting entries...")
    formatted = format_candidates(classified)
    insertions = generate_insertion_commands(formatted)

    if is_pr_mode():
        # PR body FIRST — before anything that can fail after this point,
        # so create-pull-request and artifact upload always find the file.
        log.info("PR mode — generating PR body before applying changes")
        pr_body = generate_pr_body(classified)
        pr_path = LOGS_DIR / "pr_body.md"
        with open(pr_path, "w") as f:
            f.write(pr_body)
        log.info(f"PR body saved to: {pr_path}")

        if apply_insertions(insertions):
            log.info("Changes applied successfully.")
        else:
            log.error("Failed to apply changes. PR body preserved for review.")
            sys.exit(1)
        sys.exit(0)

    # Step 7: Interactive mode — generate insertion script
    script_path = LOGS_DIR / "insert.sh"
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n\n")
        for filename, data in insertions.items():
            f.write(f"echo 'Inserting into {filename}...'\n")
            for row in data["rows"]:
                f.write(f"sed -i '/{data['pattern']}/ a\\\n{row}' {filename}\n")
        f.write("\necho '✅ Insertion complete.'\n")
    script_path.chmod(0o755)

    log.info(f"Insertion script saved to: {script_path}")
    log.info("Run: ./repo-maintenance-automation/logs/insert.sh to apply changes")

    print_banner("✅ Harvest complete. Ready for review.", "=")

if __name__ == "__main__":
    main()
