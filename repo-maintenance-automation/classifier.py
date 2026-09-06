#!/usr/bin/env python3
"""
File: classifier.py
Tool: LLMDataHub Harvester — Resource Classifier
Version: 1.0.2
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Classifies harvested repos as Dataset, Model, Paper, or Tool.
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple

# === CORPORATE BLOCKLIST ===
CORPORATE_BLOCKLIST = [
    "nvidia",
    "huggingface",
    "google",
    "microsoft",
    "meta",
    "amazon",
    "aws",
    "openai",
    "anthropic",
    "deepmind",
    "ibm",
    "intel",
    "amd",
    "apple",
    "salesforce",
    "oracle",
    "tencent",
    "alibaba",
    "baidu",
    "bytedance",
    "youtube",
    "twitch",
    "spotify",
    "netflix",
]

def is_corporate(repo: Dict) -> bool:
    full_name = repo.get("full_name", "").lower()
    owner = full_name.split("/")[0] if "/" in full_name else ""
    for corp in CORPORATE_BLOCKLIST:
        if corp in owner or corp in full_name:
            return True
    return False

# === STRONG DATASET INDICATORS (higher weight) ===
STRONG_DATASET = [
    "dataset",
    "corpus",
    "benchmark",
]

# === WEAK DATASET INDICATORS (lower weight, need multiple) ===
WEAK_DATASET = [
    "qa pairs", "question answering", "sft data", "instruction data",
    "pretraining data", "rlhf data", "dpo data", "conversational data",
    "dialogue data", "multimodal data", "vision-language data",
    "code data", "math data", "reasoning data",
    "labeled data", "annotated data", "crowdsourced data",
    "human-annotated data", "training data", "fine-tuning data",
    "collection", "examples", "samples"
]

# === MODEL INDICATORS ===
MODEL_KEYWORDS = [
    "model", "llm", "large language model", "foundation model",
    "checkpoint", "weights", "parameter", "finetuned", "fine-tuned",
    "lora", "adapter", "quantized", "gguf", "mlx", "onnx",
    "open weight", "pretrained", "pre-trained"
]

# === PAPER INDICATORS ===
PAPER_KEYWORDS = [
    "paper", "arxiv", "preprint", "publication", "research",
    "survey", "review", "benchmark", "evaluation", "analysis",
    "neurips", "icml", "iclr", "acl", "emnlp", "cvpr", "eccv", "iccv"
]

# === TOOL INDICATORS ===
TOOL_KEYWORDS = [
    "framework", "toolkit", "library", "sdk", "api", "cli",
    "dashboard", "platform", "pipeline", "workflow", "orchestrator",
    "agent", "skills", "plugin", "extension", "harness",
    "studio", "lab", "trainer", "evaluator", "deployer", "server",
    "inference", "serving", "quantization", "compression"
]

# === STRONG NOISE INDICATORS ===
NOISE_KEYWORDS = [
    "personal website", "portfolio", "blog", "profile", "resume",
    "template", "boilerplate", "demo", "example", "tutorial", "guide",
    "awesome list", "paper list", "curated list", "directory",
    "profile readme", "profile page"
]

def classify_repo(repo: Dict) -> Tuple[str, float]:
    name = repo.get("name", "") or ""
    full_name = repo.get("full_name", "") or ""
    description = repo.get("description") or ""
    topics = [t.lower() for t in repo.get("topics", [])]
    
    combined = f"{name} {full_name} {description} {' '.join(topics)}".lower()
    
    # Corporate block first
    if is_corporate(repo):
        return "corporate", 0.0
    
    # Strong noise check
    for noise in NOISE_KEYWORDS:
        if noise in combined:
            return "noise", 0.0
    
    # === Calculate scores ===
    scores = {"dataset": 0, "model": 0, "paper": 0, "tool": 0}
    
    # Strong dataset indicators
    for kw in STRONG_DATASET:
        if kw in combined:
            scores["dataset"] += 0.5
    
    # Weak dataset indicators (need multiple)
    weak_count = 0
    for kw in WEAK_DATASET:
        if kw in combined:
            weak_count += 1
    scores["dataset"] += min(weak_count * 0.1, 0.3)
    
    # Model indicators
    for kw in MODEL_KEYWORDS:
        if kw in combined:
            scores["model"] += 0.3
    
    # Paper indicators
    for kw in PAPER_KEYWORDS:
        if kw in combined:
            scores["paper"] += 0.3
    
    # Tool indicators
    for kw in TOOL_KEYWORDS:
        if kw in combined:
            scores["tool"] += 0.3
    
    # Bonus for "dataset" in repo name
    if "dataset" in name.lower():
        scores["dataset"] += 0.3
    
    # Bonus for "dataset" in topics
    if "dataset" in topics:
        scores["dataset"] += 0.2
    
    # Find best category
    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]
    
    # Minimum threshold
    if best_score < 0.3:
        return "noise", best_score
    
    return best_category, best_score

def classify_candidates(candidates: List[Dict]) -> Dict[str, List[Dict]]:
    result = {"dataset": [], "model": [], "paper": [], "tool": [], "corporate": [], "noise": []}
    for repo in candidates:
        category, score = classify_repo(repo)
        repo["_category"] = category
        repo["_score"] = score
        result[category].append(repo)
    return result

def generate_classification_report(classified: Dict[str, List[Dict]]) -> str:
    lines = []
    for category, repos in classified.items():
        if not repos:
            continue
        lines.append(f"\n## {category.upper()} ({len(repos)})")
        for repo in repos[:10]:
            stars = repo.get("stars", 0)
            desc = repo.get("description", "")[:80] if repo.get("description") else ""
            lines.append(f"  - {repo['full_name']} ({stars}★, score: {repo.get('_score', 0):.2f})")
            if desc:
                lines.append(f"    {desc}...")
        if len(repos) > 10:
            lines.append(f"  ... and {len(repos) - 10} more")
    return "\n".join(lines)

def load_existing_datasets(datasets_path: Path) -> set:
    if not datasets_path.exists():
        return set()
    with open(datasets_path, "r") as f:
        content = f.read()
    existing = set()
    github_links = re.findall(r'\[([^\]]+)\]\(https://github\.com/[^\)]+\)', content)
    existing.update(github_links)
    table_rows = re.findall(r'^\|\s*\[?([^\|\]]+)\]?.*?\|', content, re.MULTILINE)
    for row in table_rows:
        name = row.strip()
        if name and name not in ["Dataset name", "---"]:
            existing.add(name)
    return existing

def filter_candidates(candidates: List[Dict], existing: set) -> List[Dict]:
    filtered = []
    for repo in candidates:
        full_name = repo.get("full_name", "")
        name = repo.get("name", "")
        if full_name in existing or name in existing:
            continue
        filtered.append(repo)
    return filtered

def main():
    from github_scraper import scrape_github
    
    print("  🔄 Running classifier (v1.0.2 - stricter dataset filtering)...")
    candidates = scrape_github(min_stars=1, max_results=50, recent_years=3, require_license=False)
    
    datasets_path = Path.cwd() / "DATASETS.md"
    existing = load_existing_datasets(datasets_path)
    new_candidates = filter_candidates(candidates, existing)
    
    print(f"  📚 Found {len(existing)} existing entries")
    print(f"  🆕 Found {len(new_candidates)} new candidates")
    
    classified = classify_candidates(new_candidates)
    
    print(f"\n  📊 Classification Results:")
    for category, repos in classified.items():
        if repos:
            print(f"     {category}: {len(repos)}")
    
    report = generate_classification_report(classified)
    print(report)
    
    report_path = Path.cwd() / "logs" / "classification_report.txt"
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, "w") as f:
        f.write("=== CLASSIFICATION REPORT ===\n\n")
        for category, repos in classified.items():
            f.write(f"\n## {category.upper()} ({len(repos)})\n")
            for repo in repos:
                f.write(f"- {repo['full_name']} ({repo['stars']}★)\n")
                f.write(f"  Score: {repo.get('_score', 0):.2f}\n")
                f.write(f"  URL: {repo['url']}\n")
                desc = repo.get('description', '') or ''
                if desc:
                    f.write(f"  Description: {desc[:200]}\n")
                f.write("\n")
    
    print(f"\n  📄 Full report saved to: {report_path}")

if __name__ == "__main__":
    main()
