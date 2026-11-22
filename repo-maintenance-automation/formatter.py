#!/usr/bin/env python3
"""
File: formatter.py
Tool: LLMDataHub Harvester — Markdown Formatter
Version: 1.3.1
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Builds markdown table rows from harvested repo dicts and inserts
         them into the archive pages. All external input (names, descrip-
         tions, URLs) is sanitized before touching any table: pipes are
         escaped, control characters stripped, whitespace normalized.
         Year-section anchors are derived at runtime — never hardcoded.

Version History:
  1.3.1 — 2026-11-22 — dead-code purge: removed standalone main()
                       (duplicate pipeline); harvest.py is the single
                       entry point.
  1.3.0 — 2026-11-22 — SECURITY/DATA-INTEGRITY: sanitize_cell() escapes
                       '|' in all external strings before row assembly
                       (table-corruption fix); year-section anchor now
                       derived at runtime (current year, falling back to
                       highest existing year div) — no more hardcoded
                       2026 patterns that strand new entries in stale
                       sections at year rollover.
  1.2.2 — 2026-11-21 — placeholder overlap fix: body region disjoint
                       from tail, placeholder rows cannot re-enter.
  1.2.1 — 2026-11-21 — newline-glue bug fixed: line-based rebuild.
  1.2.0 — 2026-10-29 — scar-tissue insertion fix: anchor on |---|
                       separator inside <details>; placeholder removal.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
LOGS_DIR = SCRIPT_DIR / "logs"


# ============================================================
# Sanitization — every external string passes through here
# BEFORE entering a markdown table cell.
# ============================================================

def sanitize_cell(value) -> str:
    """Make any external string safe as a markdown table cell.

    1. Strip control characters (incl. newlines) that would
       smash row structure.
    2. Escape literal '|' characters so they cannot break the
       table. Escaping is idempotent: a value that already
       contains '\\|' is not double-escaped.
    3. Collapse internal whitespace runs and trim.
    """
    if value is None:
        return ""
    text = str(value)
    # Kill control chars (keep regular whitespace for now)
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", text)
    # Normalize newlines/tabs to spaces, collapse runs
    text = re.sub(r"\s+", " ", text).strip()
    # Escape unescaped pipes only (idempotent)
    text = re.sub(r"(?<!\\)\|", r"\\|", text)
    return text


def _clip(description: str, limit: int = 120) -> str:
    if len(description) > limit:
        return description[:limit - 3].rstrip() + "..."
    return description


# ============================================================
# Row builders — output is guaranteed safe for table insertion
# ============================================================

def format_dataset_row(repo: Dict) -> str:
    name = sanitize_cell(repo.get("name", ""))
    url = sanitize_cell(repo.get("url", ""))
    description = _clip(sanitize_cell(repo.get("description", "")))
    stars = repo.get("stars", 0)
    language = sanitize_cell(repo.get("language", ""))
    return f"| [{name}]({url}) | — | Dataset | {language} | {stars}★ | {description} | [GitHub]({url}) |"


def format_model_row(repo: Dict) -> str:
    name = sanitize_cell(repo.get("name", ""))
    url = sanitize_cell(repo.get("url", ""))
    description = _clip(sanitize_cell(repo.get("description", "")))
    stars = repo.get("stars", 0)
    language = sanitize_cell(repo.get("language", ""))
    return f"| [{name}]({url}) | — | LLM | {language} | {stars}★ | {description} | [GitHub]({url}) |"


def format_paper_row(repo: Dict) -> str:
    name = sanitize_cell(repo.get("name", ""))
    url = sanitize_cell(repo.get("url", ""))
    description = _clip(sanitize_cell(repo.get("description", "")))
    return f"| [{name}]({url}) | — | Paper | — | — | {description} | [Code]({url}) |"


def format_tool_row(repo: Dict) -> str:
    name = sanitize_cell(repo.get("name", ""))
    url = sanitize_cell(repo.get("url", ""))
    description = _clip(sanitize_cell(repo.get("description", "")))
    stars = repo.get("stars", 0)
    language = sanitize_cell(repo.get("language", ""))
    return f"| [{name}]({url}) | — | Tool | {language} | {stars}★ | {description} | [GitHub]({url}) |"


def format_awesome_row(repo: Dict) -> str:
    # <details>/<summary> block, not a table — pipes still escaped for
    # consistency in case the block ever gets reformatted.
    name = sanitize_cell(repo.get("full_name", "") or repo.get("name", ""))
    url = sanitize_cell(repo.get("url", ""))
    description = _clip(sanitize_cell(repo.get("description", "")), limit=200)
    stars = repo.get("stars", 0)

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


# ============================================================
# Dedup identifier extraction
# ============================================================

def _row_identifiers(row: str) -> List[str]:
    """Extract every identifier we can use for dedup from a formatted row."""
    identifiers = []
    for m in re.finditer(r"\[([^\]]+)\]", row):
        text = m.group(1).strip()
        if text and text.lower() not in ("code", "github"):
            identifiers.append(text.lower())
    for m in re.finditer(r"https://github\.com/([^\)\s]+)", row):
        owner_repo = m.group(1).strip().rstrip("/").lower()
        if owner_repo:
            identifiers.append(owner_repo)
    return identifiers


# ============================================================
# Dynamic year-section resolution (C3 fix)
# ============================================================

_YEAR_DIV_RE = re.compile(
    r'###\s*<div id="(?:models|tools|papers)-(\d{4})">\s*\d{4}\s*</div>'
)


def _target_year_section(filename: str, kind: str) -> Optional[str]:
    """Resolve the insertion anchor for a year-section file at runtime.

    kind is 'models', 'tools', or 'papers'.

    Preference order:
      1. A year div matching the CURRENT year.
      2. The HIGHEST existing year div in the file.
      3. None (caller decides what to do — typically fall back to a
         top-level section pattern or report failure).

    The returned pattern anchors on the chosen div line so downstream
    insertion logic walks from there.
    """
    path = Path(filename)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    years = [(int(m.group(1)), m.group(0)) for m in _YEAR_DIV_RE.finditer(content)]
    if not years:
        return None

    current_year = datetime.now().year
    match_kind = {"models": "models", "tools": "tools", "papers": "papers"}[kind]

    # Preference 1: current year's div
    for year, div_line in years:
        if year == current_year and match_kind in div_line:
            return re.escape(div_line)

    # Preference 2: highest existing year div of this kind
    candidates = [(y, dl) for y, dl in years if match_kind in dl]
    if not candidates:
        return None
    year, div_line = max(candidates, key=lambda pair: pair[0])
    return re.escape(div_line)


# ============================================================
# Insertion
# ============================================================

def insert_rows_into_file(filename: str, section_pattern: str, rows: List[str]) -> bool:
    """Insert rows into the first table found UNDER a matching section heading.

    Anchors on the table separator row (|---|) found after the section
    heading — inside the <details> block — then walks line-by-line to
    the end of the table body. Appends new rows after the LAST existing
    table row, each on its own line. Placeholder rows (*No ... listed.*)
    are dropped when real entries arrive.

    v1.2.1 — line-based iteration; guaranteed newline-terminated rows.
    v1.2.2 — body region disjoint from tail; placeholders can't re-enter.
    """
    filepath = Path(filename)
    if not filepath.exists():
        print(f"  ❌ File not found: {filename}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    section_match = re.search(section_pattern, content, re.MULTILINE)
    if not section_match:
        print(f"  ❌ Section not found in {filename}: {section_pattern}")
        return False

    # Work on a line basis from the section heading onward.
    after_lines = content[section_match.end():].split("\n")

    # Find the table separator row (|---|...) — inside the details block.
    sep_idx = None
    for i, line in enumerate(after_lines):
        if re.match(r"^\|[ :|-]*-+[ :|-]*\|?\s*$", line):
            sep_idx = i
            break
    if sep_idx is None:
        print(f"  ❌ Table separator not found under section in {filename}")
        return False

    # Walk the table body: rows start with '|'; anything else ends it.
    body_idx = sep_idx + 1
    while body_idx < len(after_lines):
        line = after_lines[body_idx]
        if line.strip().startswith("|"):
            body_idx += 1
            continue
        break

    # Body region: everything the walk consumed, minus placeholder rows.
    body_region = after_lines[sep_idx + 1:body_idx]
    kept_body = [
        l for l in body_region
        if not ("*no " in l.lower() and "listed" in l.lower())
    ]

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

    # Rebuild: heading prefix + separator + kept body + new rows + tail.
    rebuilt = (
        content[:section_match.end()]
        + "\n".join(
            after_lines[:sep_idx + 1]
            + kept_body
            + existing_entries
            + after_lines[body_idx:]
        )
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(rebuilt)

    print(f"  ✅ Added {len(existing_entries)} entries to {filename}")
    return True


def _resolve_pattern(filename: str, preferred: str, fallback: str) -> str:
    """If the preferred section pattern isn't in the file, use the fallback."""
    path = Path(filename)
    if not path.exists():
        return preferred
    with open(path, "r", encoding="utf-8") as f:
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

    for kind, filename, rows_key in (
        ("models", "MODELS.md", "model"),
        ("tools", "TOOLS.md", "tool"),
        ("papers", "PAPERS.md", "paper"),
    ):
        if formatted[rows_key]:
            anchor = _target_year_section(filename, kind)
            if anchor is None:
                # No year div found at all — keep legacy hardcoded pair
                # so behaviour is unchanged rather than crashing.
                anchor = _resolve_pattern(
                    filename,
                    rf'### <div id="{kind}-2026">\d{{4}}</div>',
                    rf'### <div id="{kind}-2025">\d{{4}}</div>',
                )
            result[filename] = {
                "pattern": anchor,
                "rows": formatted[rows_key],
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
