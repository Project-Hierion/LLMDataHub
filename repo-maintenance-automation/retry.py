#!/usr/bin/env python3
"""
File: retry.py
Tool: LLMDataHub Harvester — Retry Utilities
Version: 1.0.0
System: Project Hierion / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Exponential backoff with jitter for transient HTTP failures.
         Retries 429/5xx and connection errors. Raises immediately on
         permanent errors (403 with no reset time, 422, 404).
"""

import functools
import random
import time
import requests

RETRYABLE_STATUS = {429, 500, 502, 503, 504}

def with_retry(max_attempts: int = 4, base_delay: float = 2.0, max_delay: float = 60.0, logger=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as exc:
                    resp = getattr(exc, "response", None)
                    status = getattr(resp, "status_code", None)
                    if status is not None and status not in RETRYABLE_STATUS:
                        raise  # permanent — don't waste attempts
                    last_exc = exc
                except (TimeoutError, ConnectionError) as exc:
                    last_exc = exc

                if attempt == max_attempts:
                    break
                delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                delay += random.uniform(0, delay * 0.25)  # jitter avoids thundering herd
                if logger:
                    logger.warning(f"Attempt {attempt}/{max_attempts} failed ({type(last_exc).__name__}); retrying in {delay:.1f}s")
                time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator
