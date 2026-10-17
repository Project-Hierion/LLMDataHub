# Repo Maintenance Automation

Automation suite for LLMDataHub: autonomous harvesting, validation, and
archive maintenance. System: Project Hierion. License: AGPLv3 with
Commons Clause.

## Components

| File | Purpose |
|------|---------|
| `harvest.py` | Main orchestrator. Scrapes, classifies, formats, inserts. |
| `github_scraper.py` | GitHub API search with rate limiting and retry. |
| `classifier.py` | Keyword scoring: dataset / model / paper / tool / noise. |
| `formatter.py` | Formats rows and inserts them into archive pages. |
| `validate-autonomy.py` | Vault health check (structure, HF-links, placeholders). |
| `logger.py` | Structured JSONL logging with run-ID correlation. |
| `retry.py` | Exponential backoff for transient HTTP failures. |
| `config.yaml` | Validation rules and required sections. |

## Where Things Live

- **Logs & reports:** `repo-maintenance-automation/logs/`
  - `classification_report.txt` — full harvest results
  - `pr_body.md` — pull request body for the harvest PR
  - `run_<run_id>.jsonl` — structured log for each run
  - `rejected_candidates.txt` — the skip-list (persistent)
  - `vault_health_report.txt` — validator output
    
- **Workflows:**
  - `.github/workflows/harvest.yml` (weekly harvest, Thursdays 05:00 UTC)
  - `.github/workflows/vault-check.yml` (validation on push/PR)

## How the Harvest Works

1. Weekly cron runs `harvest.py --pr` via GitHub Actions
2. Scraper searches GitHub (keywords, ≥20★, updated within 3 years, corporate blocklist)
3. Classifier sorts candidates into buckets; skip-list and archive dedup filter repeats
4. Report is written, PR body generated, entries inserted into archive pages
5. `peter-evans/create-pull-request@v6` opens a PR on branch `auto/harvest-N`
6. Logs upload as an artifact (`harvest-report-<run_id>`)

**Nothing hits `main` without human review. Merge = approve, close = reject, edit = cherry-pick.**

## Manual Procedure: Pruning a Harvest PR

When a harvest PR lands and you want to keep some entries and drop
others:

### 1. Fetch and checkout the PR branch

```bash
git fetch origin auto/harvest-NN
git checkout auto/harvest-NN
```

If git refuses due to a dirty log file (they change every run):

git checkout -- repo-maintenance-automation/logs/classification_report.txt
git checkout auto/harvest-NN

### 2. Inspect what the batch added

```bash
git diff main -- TOOLS.md | grep '^+' | head -20
git diff main -- MODELS.md | grep '^+' | head -20
git diff main -- PAPERS.md | grep '^+' | head -20
git diff main -- DATASETS.md | grep '^+' | head -20
```

### 3. Add rejected repos to the skip-list

Every rejected repo MUST go on the skip-list, or next week's harvest will find it again. Entries live in repo-maintenance-automation/logs/rejected_candidates.txt, one per line, format owner/repo  # reason:

```bash
sed -i '/# === Off-theme/i\
owner/repo  # short reason it was rejected\
owner2/repo2  # short reason' \
  repo-maintenance-automation/logs/rejected_candidates.txt
```

Categories: License issues, Off-theme, Unclear/borderline.

Sanity check: every row you delete in step 4 should appear here.

### 4. Delete unwanted rows from the archive pages

Delete the table rows for rejected entries (match on the repo URL slug):

```bash
sed -i '/owner\/repo/d;/owner2\/repo2/d' TOOLS.md
```

### 5. Verify

```bash
git diff main -- TOOLS.md | grep '^+'
```

Expect only the header line and keepers' rows.

### 6. Commit, push, merge

```bash
git add MODELS.md PAPERS.md TOOLS.md DATASETS.md \
  repo-maintenance-automation/logs/rejected_candidates.txt
git commit -m "chore: prune harvest #N — removed off-theme entries, updated skip-list"
git push --force-with-lease origin auto/harvest-NN
```

Then merge the PR on GitHub. Done — the keepers are archived, the junk is blocked forever.

## Reference: Harvest-Related Paths
- PR branch pattern: auto/harvest-<run_number>
- Skip-list: repo-maintenance-automation/logs/rejected_candidates.txt
- Artifacts: per-run, named harvest-report-<run_id>
- Structured logs: run_<run_id>.jsonl in this directory's logs/

## Future Work (Parking Lot)
- Second pipeline — "Deep Harvest": targeted scraping beyond GitHub (ModelScope, arXiv, university/government data portals) with strict anti-noise filtering: no social media, blocklist low-value domains, require data-file signatures, enforce license checks. Keep the GitHub pipeline lean; this is a separate system.
- Deferred hardening (Option C): typed exceptions, post-insertion verification, test suite, concurrency lock.
- Decision pending: whether logs/ should remain tracked in git as an audit trail or be gitignored (artifact-only).
