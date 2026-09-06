#!/usr/bin/env python3
"""
File: harvest.py
Tool: LLMDataHub Harvester — Main Orchestrator
Version: 1.0.1
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause
"""

import sys
import time
import json
import os
from pathlib import Path
from typing import List, Dict

from github_scraper import scrape_github
from classifier import classify_candidates, filter_candidates, load_existing_datasets
from formatter import format_candidates, generate_insertion_commands

def print_banner(text: str, char: str = "=", width: int = 60):
    print(f"\n{char * width}")
    print(f"  {text}")
    print(f"{char * width}\n")

def is_pr_mode() -> bool:
    """Check if running in PR mode (non-interactive)."""
    return "--pr" in sys.argv or os.environ.get("GITHUB_ACTIONS") == "true"

def human_review(classified: Dict[str, List[Dict]]) -> bool:
    """Present the report and ask for human approval."""
    total = sum(len(repos) for repos in classified.values())
    
    print_banner("🌱 HARVEST COMPLETE", "=")
    
    print(f"  📊 Summary:")
    for category, repos in classified.items():
        if repos:
            print(f"     {category}: {len(repos)}")
    print(f"     TOTAL: {total}")
    
    print(f"\n  📄 Full report: logs/classification_report.txt")
    
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
        print("\n  🤖 Running in PR mode — auto-approving for PR generation")
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
    """Generate a PR body from the classified results."""
    lines = [
        "## 🌱 Weekly Harvest\n",
        "Automated harvest of new open-source LLM resources.\n",
        "### What Was Found\n",
    ]
    
    for category, repos in classified.items():
        if repos:
            lines.append(f"- **{category.capitalize()}:** {len(repos)}")
    
    lines.append("\n### Review Instructions")
    lines.append("1. Check the report in `logs/classification_report.txt`")
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
    print_banner("🌱 LLMDataHub Harvester", "=")
    
    # Step 1: Scrape
    print("  📡 Scraping GitHub for candidates...")
    candidates = scrape_github(min_stars=20, max_results=100, recent_years=3, require_license=False)
    
    # Step 2: Dedupe
    datasets_path = Path.cwd() / "DATASETS.md"
    existing = load_existing_datasets(datasets_path)
    new_candidates = filter_candidates(candidates, existing)
    print(f"  📚 Found {len(existing)} existing entries, {len(new_candidates)} new candidates")
    
    # Step 3: Classify
    print("  🏷️  Classifying candidates...")
    classified = classify_candidates(new_candidates)
    
    # Step 4: Save report
    report_path = Path.cwd() / "logs" / "classification_report.txt"
    report_path.parent.mkdir(exist_ok=True)
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
    
    print(f"  📄 Report saved to: {report_path}")
    
    # Step 5: Human review (or PR mode)
    if not human_review(classified):
        print("  ❌ Rejected by user. Logging and exiting.")
        log_path = Path.cwd() / "logs" / "harvest_rejected.txt"
        log_path.parent.mkdir(exist_ok=True)
        with open(log_path, "w") as f:
            f.write(f"Harvest rejected at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for category, repos in classified.items():
                if repos:
                    f.write(f"\n{category.upper()}: {len(repos)}\n")
                    for repo in repos:
                        f.write(f"  - {repo['full_name']}\n")
        print(f"  📄 Log saved to: {log_path}")
        sys.exit(0)
    
    # Step 6: Generate PR body if in PR mode
    if is_pr_mode():
        pr_body = generate_pr_body(classified)
        pr_path = Path.cwd() / "logs" / "pr_body.md"
        pr_path.parent.mkdir(exist_ok=True)
        with open(pr_path, "w") as f:
            f.write(pr_body)
        print(f"  📄 PR body saved to: {pr_path}")
        print("  🤖 PR mode — exiting without making changes")
        sys.exit(0)
    
    # Step 7: Interactive mode — generate insertion script
    print("  ✏️  Formatting and inserting entries...")
    formatted = format_candidates(classified)
    commands = generate_insertion_commands(formatted)
    
    script_path = Path.cwd() / "logs" / "insert.sh"
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n\n")
        for filename, command in commands.items():
            f.write(f"echo 'Inserting into {filename}...'\n")
            f.write(command + "\n")
        f.write("\necho '✅ Insertion complete.'\n")
    script_path.chmod(0o755)
    
    print(f"  📄 Insertion script saved to: {script_path}")
    print("  Run: ./logs/insert.sh to apply changes")
    
    print_banner("✅ Harvest complete. Ready for review.", "=")

if __name__ == "__main__":
    main()
