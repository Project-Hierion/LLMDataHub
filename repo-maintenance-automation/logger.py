#!/usr/bin/env python3
"""
File: logger.py
Tool: LLMDataHub Harvester — Structured Logger
Version: 1.0.0
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Centralized logging with run-ID correlation. Every run gets
         one JSON-lines file in logs/ (run_<run_id>.jsonl) plus
         human-readable console output. In CI, run_id comes from
         GITHUB_RUN_ID so logs join 1:1 with the Actions run.
"""

import json
import logging
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LOGS_DIR = SCRIPT_DIR / "logs"

def _make_run_id() -> str:
    if os.environ.get("GITHUB_RUN_ID"):
        return f"gha-{os.environ['GITHUB_RUN_ID']}-{os.environ.get('GITHUB_RUN_ATTEMPT', '1')}"
    return f"local-{uuid.uuid4().hex[:12]}"

RUN_ID = os.environ.get("HARVEST_RUN_ID") or _make_run_id()
os.environ["HARVEST_RUN_ID"] = RUN_ID  # propagate to child processes

class JsonFormatter(logging.Formatter):
    """One JSON object per line — greppable, jq-able, replayable."""
    def format(self, record):
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "run_id": RUN_ID,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(f"[%(levelname)s][{RUN_ID[-12:]}] %(message)s"))
    logger.addHandler(console)

    file_handler = logging.FileHandler(LOGS_DIR / f"run_{RUN_ID}.jsonl")
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)
    return logger
