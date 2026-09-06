#!/usr/bin/env python3
"""
File: formatter.py
Tool: LLMDataHub Harvester — Markdown Formatter
Version: 1.0.1
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Formats classified repo candidates as markdown table rows
         for DATASETS.md, MODELS.md, PAPERS.md, or TOOLS.md.
"""

from typing import Dict, List

def safe_string(value) -> str:
    """Safely convert a value to a string, handling None."""
    if value is None:
        return ""
    return str(value).strip()

def format_dataset_row(repo: Dict) -> str:
    """Format a dataset repo as a markdown table row."""
    name = safe_string(repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)
    license_name = safe_string(repo.get("license", "unknown"))
    language = safe_string(repo.get("language", ""))
    
    if len(description) > 120:
        description = description[:117] + "..."
    
    return f"| [{name}]({url}) | — | Dataset | {language} | {stars}★ | {description} |"

def format_model_row(repo: Dict) -> str:
    """Format a model repo as a markdown table row."""
    name = safe_string(repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)
    license_name = safe_string(repo.get("license", "unknown"))
    language = safe_string(repo.get("language", ""))
    
    if len(description) > 120:
        description = description[:117] + "..."
    
    return f"| [{name}]({url}) | — | LLM | {language} | {stars}★ | {description} |"

def format_paper_row(repo: Dict) -> str:
    """Format a paper repo as a markdown table row."""
    name = safe_string(repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)
    
    if len(description) > 120:
        description = description[:117] + "..."
    
    return f"| [{name}]({url}) | — | — | [Code]({url}) | — | {description} |"

def format_tool_row(repo: Dict) -> str:
    """Format a tool repo as a markdown table row."""
    name = safe_string(repo.get("name", ""))
    url = safe_string(repo.get("url", ""))
    description = safe_string(repo.get("description", ""))
    stars = repo.get("stars", 0)
    language = safe_string(repo.get("language", ""))
    
    if len(description) > 120:
        description = description[:117] + "..."
    
    return f"| [{name}]({url}) | — | Tool | {language} | {description} |"

def format_candidates(classified: Dict[str, List[Dict]]) -> Dict[str, List[str]]:
    """Format each category's candidates into markdown rows."""
    result = {
        "dataset": [],
        "model": [],
        "paper": [],
        "tool": [],
    }
    
    for repo in classified.get("dataset", []):
        result["dataset"].append(format_dataset_row(repo))
    
    for repo in classified.get("model", []):
        result["model"].append(format_model_row(repo))
    
    for repo in classified.get("paper", []):
        result["paper"].append(format_paper_row(repo))
    
    for repo in classified.get("tool", []):
        result["tool"].append(format_tool_row(repo))
    
    return result

def generate_insertion_commands(formatted: Dict[str, List[str]]) -> Dict[str, str]:
    """Generate sed commands to insert rows into the appropriate files."""
    commands = {}
    
    if formatted["dataset"]:
        rows = "\n".join(formatted["dataset"])
        commands["DATASETS.md"] = f"sed -i '/### Datasets Released in 2025/ a\\\n{rows}' DATASETS.md"
    
    if formatted["model"]:
        rows = "\n".join(formatted["model"])
        commands["MODELS.md"] = f"sed -i '/### <div id=\"models-2025\">2025<\\/div>/ a\\\n{rows}' MODELS.md"
    
    if formatted["paper"]:
        rows = "\n".join(formatted["paper"])
        commands["PAPERS.md"] = f"sed -i '/### <div id=\"papers-2025\">2025<\\/div>/ a\\\n{rows}' PAPERS.md"
    
    if formatted["tool"]:
        rows = "\n".join(formatted["tool"])
        commands["TOOLS.md"] = f"sed -i '/### <div id=\"tools-2025\">2025<\\/div>/ a\\\n{rows}' TOOLS.md"
    
    return commands

def main():
    from classifier import classify_candidates
    from github_scraper import scrape_github
    from pathlib import Path
    
    print("  🔄 Running formatter...")
    
    candidates = scrape_github(min_stars=1, max_results=100, recent_years=3, require_license=False)
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
    
    commands = generate_insertion_commands(formatted)
    print(f"\n  📝 Insertion Commands:")
    for filename, command in commands.items():
        print(f"    {filename}: {command[:80]}...")
    
    commands_path = Path.cwd() / "logs" / "insertion_commands.txt"
    commands_path.parent.mkdir(exist_ok=True)
    with open(commands_path, "w") as f:
        for filename, command in commands.items():
            f.write(f"# {filename}\n")
            f.write(command)
            f.write("\n\n")
    
    print(f"\n  📄 Commands saved to: {commands_path}")

if __name__ == "__main__":
    main()
