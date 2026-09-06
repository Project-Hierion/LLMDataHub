#!/usr/bin/env python3
"""
File: audit.py
Tool: LLMDataHub Harvester — Audit Logger
Version: 1.0.0
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause
"""

import json
import hashlib
import os
from datetime import datetime
from pathlib import Path

def audit_log(action: str, data: dict, result: str = "success") -> None:
    """Log all actions for accountability."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "data_hash": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest(),
        "result": result,
        "source": os.environ.get("GITHUB_ACTIONS", "local"),
        "runner": os.environ.get("RUNNER_NAME", "unknown"),
    }
    
    with open(log_dir / "audit.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # Also log to a human-readable file
    with open(log_dir / "audit_readable.log", "a") as f:
        f.write(f"[{entry['timestamp']}] {action} → {result} (hash: {entry['data_hash'][:8]})\n")
