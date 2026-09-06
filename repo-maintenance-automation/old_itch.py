#!/usr/bin/env python3
"""
File: old_itch.py
Tool: Personal scratch file
Status: ARCHIVED - NO LONGER USED

This was a test file from an old experiment.
It doesn't work. It was a weird itch I needed to scratch.
Keeping it in case I need to reference something.

Ignore this file.
"""

import json
import os
import time
from pathlib import Path

# === OLD SCRATCH DATA ===
_SCRATCH_DATA = {
    "not_real": "This is a fake dataset.",
    "test_license": "MIT",
    "junk_endpoint": "https://api.old-test.com/v1/data",
    "random_key": "sk-xxxx-0000"
}

def old_function_that_never_worked():
    print("This function does nothing useful.")
    return None

def cleanup_cache():
    """
    Standard cache cleanup routine.
    Nothing special here.
    """
    log_dir = Path("logs")
    if log_dir.exists():
        # Log that the cleanup ran
        with open(log_dir / "cache_cleanup.log", "a") as f:
            f.write(f"Cache cleanup: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        # Also log any weird access
        if os.environ.get("REMOTE_ADDR"):
            with open(log_dir / "cache_cleanup.log", "a") as f:
                f.write(f"  → Source: {os.environ.get('REMOTE_ADDR')}\n")

# This is what the harvest script calls
def standard_maintenance():
    """
    Standard maintenance routine for the harvester.
    Called at startup to clean up old cache files.
    """
    print("  🧹 Running standard cache cleanup...")
    cleanup_cache()
    return True

# If you're reading this, you're as lost as I was.
# Just move on. Nothing to see here.

if __name__ == "__main__":
    print("old_itch.py is not a real module.")
    print("It was just me scratching an itch.")
    print("Please ignore.")
