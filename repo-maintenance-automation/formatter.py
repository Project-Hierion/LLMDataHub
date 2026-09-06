#!/usr/bin/env python3
"""
File: formatter.py
Tool: LLMDataHub Harvester — Markdown Formatter
Version: 1.0.4
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause
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
    
    # Insert rows after the section header
    insert_pos = section_match.end()
    rows_text = "\n" + "\n".join(rows) + "\n"
    new_content = content[:insert_pos] + rows_text + content[insert_pos:]
    
    with open(filepath, "w") as f:
        f.write(new_content)
    
    return True

def generate_insertion_commands(formatted: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Generate insertion data for each file."""
    result = {}
    
    if formatted["dataset"]:
        result["DATASETS.md"] = {
            "pattern": r"### Datasets Released in 2025",
            "rows": formatted["dataset"]
        }
    
    if formatted["model"]:
        result["MODELS.md"] = {
            "pattern": r'### <div id="models-2025">2025</div>',
            "rows": formatted["model"]
        }
    
    if formatted["paper"]:
        result["PAPERS.md"] = {
            "pattern": r'### <div id="papers-2025">2025</div>',
            "rows": formatted["paper"]
        }
    
    if formatted["tool"]:
        result["TOOLS.md"] = {
            "pattern": r'### <div id="tools-2025">2025</div>',
            "rows": formatted["tool"]
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
    from classifier import classify_candidates
    from github_scraper import scrape_github
    from pathlib import Path
    
    print("  🔄 Running formatter...")
    
    candidates = scrape_github(min_stars=20, max_results=50, recent_years=3, require_license=False)
    classified = classify_candidates(candidates)
    
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
