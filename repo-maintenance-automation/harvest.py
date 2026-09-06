#!/usr/bin/env python3
"""
File: harvest.py
Tool: LLMDataHub Harvester — Main Orchestrator
Version: 1.0.0
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Orchestrates the full harvest pipeline with human-in-the-loop review.
         Scrape → Classify → Report → PAUSE → [Yes/No/Exit]
"""

import sys
import time
from pathlib import Path
from typing import List, Dict

from github_scraper import scrape_github
from classifier import classify_candidates, filter_candidates, load_existing_datasets
from formatter import format_candidates, generate_insertion_commands

def print_banner(text: str, char: str = "=", width: int = 60):
    print(f"\n{char * width}")
    print(f"  {text}")
    print(f"{char * width}\n")

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
    
    # Show top candidates
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

def main():
    print_banner("🌱 LLMDataHub Harvester", "=")
    
    # Step 1: Scrape
    print("  📡 Scraping GitHub for candidates...")
    candidates = scrape_github(min_stars=1, max_results=100, recent_years=3, require_license=False)
    
    # Step 2: Dedupe
    datasets_path = Path.cwd() / "DATASETS.md"
    existing = load_existing_datasets(datasets_path)
    new_candidates = filter_candidates(candidates, existing)
    print(f"  📚 Found {len(existing)} existing entries, {len(new_candidates)} new candidates")
    
    # Step 3: Classify
    print("  🏷️  Classifying candidates...")
    classified = classify_candidates(new_candidates)
    
    # Step 4: Human review
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
    
    # Step 5: Format and insert
    print("  ✏️  Formatting and inserting entries...")
    formatted = format_candidates(classified)
    commands = generate_insertion_commands(formatted)
    
    # Step 6: Execute insertion commands
    for filename, command in commands.items():
        print(f"     Inserting into {filename}...")
        # Write command to a shell script instead of executing directly
        # This gives us a chance to review before applying
        script_path = Path.cwd() / "logs" / "insert.sh"
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\n\n")
            for fname, cmd in commands.items():
                f.write(f"echo 'Inserting into {fname}...'\n")
                f.write(cmd + "\n")
            f.write("\necho '✅ Insertion complete.'\n")
        script_path.chmod(0o755)
        print(f"  📄 Insertion script saved to: {script_path}")
        print("  Run: ./logs/insert.sh to apply changes")
    
    print_banner("✅ Harvest complete. Ready for review.", "=")

if __name__ == "__main__":
    main()
