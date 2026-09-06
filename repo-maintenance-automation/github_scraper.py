#!/usr/bin/env python3
"""
File: github_scraper.py
Tool: LLMDataHub Harvester — GitHub API Scraper
Version: 1.0.3
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause
"""

import os
import re
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

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

SEARCH_KEYWORDS = [
    # Existing
    "dataset",
    "llm dataset",
    "sft dataset",
    "instruction tuning dataset",
    "pretraining dataset",
    "rlhf dataset",
    "dpo dataset",
    "chat dataset",
    "conversational dataset",
    "multimodal dataset",
    "vision dataset",
    "code dataset",
    "math dataset",
    "reasoning dataset",
    # New additions for awesome lists and curation
    "awesome list",
    "curated list",
    "post-training",
    "fine-tuning",
    "preference",
    "alignment",
    "llm course",
    "llm resources",
]

PERMISSIVE_LICENSES = [
    "mit",
    "apache-2.0",
    "bsd-3-clause",
    "bsd-2-clause",
    "cc0-1.0",
    "cc-by-4.0",
    "cc-by-sa-4.0",
    "odc-by",
    "unlicense",
]

def search_github(query: str, max_results: int = 100) -> List[Dict]:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    all_results = []
    page = 1
    per_page = 30
    
    while len(all_results) < max_results:
        url = f"{GITHUB_API}/search/repositories"
        params = {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 403:
                reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                if reset_time:
                    wait_time = max(0, reset_time - int(time.time())) + 5
                    print(f"  ⏳ Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"  ❌ Rate limited. No reset time provided.")
                    break
            
            if response.status_code == 422:
                print(f"  ⚠️ 422 error on query: {query[:60]}...")
                break
            
            if response.status_code != 200:
                print(f"  ❌ GitHub API error: {response.status_code}")
                break
            
            data = response.json()
            items = data.get("items", [])
            if not items:
                break
            
            for repo in items:
                license_info = repo.get("license")
                license_name = license_info.get("key", "") if license_info else ""
                repo_data = {
                    "name": repo.get("name", ""),
                    "full_name": repo.get("full_name", ""),
                    "description": repo.get("description", ""),
                    "url": repo.get("html_url", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "license": license_name,
                    "license_url": license_info.get("url", "") if license_info else "",
                    "language": repo.get("language", ""),
                    "updated_at": repo.get("updated_at", ""),
                    "created_at": repo.get("created_at", ""),
                    "topics": repo.get("topics", []),
                }
                all_results.append(repo_data)
            
            if len(items) < per_page:
                break
            
            page += 1
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request error: {e}")
            break
    
    return all_results[:max_results]

def is_recently_updated(repo: Dict, years: int = 3) -> bool:
    updated_at = repo.get("updated_at", "")
    if not updated_at:
        return False
    try:
        updated_date = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        cutoff_date = datetime.now().replace(tzinfo=updated_date.tzinfo) - timedelta(days=years*365)
        return updated_date > cutoff_date
    except:
        return False

def has_permissive_license(repo: Dict) -> bool:
    license_name = repo.get("license", "").lower()
    for lic in PERMISSIVE_LICENSES:
        if lic in license_name:
            return True
    return False

def scrape_github(
    keywords: List[str] = None,
    min_stars: int = 20,
    max_results: int = 100,
    recent_years: int = 3,
    require_license: bool = False,
) -> List[Dict]:
    if keywords is None:
        keywords = SEARCH_KEYWORDS
    
    all_candidates = []
    seen_repos = set()
    
    cutoff_date = (datetime.now() - timedelta(days=recent_years*365)).strftime("%Y-%m-%d")
    
    print(f"  🔍 Scanning GitHub for dataset repos...")
    print(f"     Keywords: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
    print(f"     Min stars: {min_stars}, Recent: {recent_years} years (since {cutoff_date})")
    
    for keyword in keywords:
        query = f'{keyword} in:description,readme pushed:>{cutoff_date}'
        if require_license:
            query += ' license:mit license:apache-2.0 license:bsd-3-clause'
        
        print(f"     Query: {query[:80]}...")
        results = search_github(query, max_results=50)
        
        for repo in results:
            repo_key = repo["full_name"]
            if repo_key in seen_repos:
                continue
            seen_repos.add(repo_key)
            
            # Skip corporate
            if is_corporate(repo):
                continue
            
            if repo["stars"] < min_stars:
                continue
            if not is_recently_updated(repo, recent_years):
                continue
            if require_license and not has_permissive_license(repo):
                continue
            
            all_candidates.append(repo)
        
        time.sleep(1)
    
    print(f"  ✅ Found {len(all_candidates)} candidates after filtering")
    return all_candidates

if __name__ == "__main__":
    candidates = scrape_github(min_stars=20, max_results=20, recent_years=3, require_license=False)
    print(f"\n  Candidates:")
    for repo in candidates[:10]:
        print(f"    - {repo['full_name']} ({repo['stars']}★) — {repo.get('license', 'no license')}")
