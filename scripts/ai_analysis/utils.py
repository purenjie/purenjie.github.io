"""Utility helpers for the AI analysis pipeline.

Includes:
- Frontmatter parsing
- MD5 hashing
- IO-safe JSON read/write
- Jieba-based top words
- Sentence stats helpers
- Co-occurrence network construction
- Simple retry decorator
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from functools import wraps
from pathlib import Path
from typing import Callable, Dict, List, Tuple


def md5_hash_text(text: str) -> str:
    m = hashlib.md5()
    m.update(text.encode("utf-8"))
    return m.hexdigest()


def parse_frontmatter_and_body(path: Path) -> Tuple[Dict, str]:
    """Parse YAML frontmatter and return (meta, body).

    This function does not depend on PyYAML to avoid strict YAML errors.
    It simply extracts the frontmatter block and returns it as best-effort key-values.
    """
    text = path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\n([\s\S]*?)\n---\s*\n?", text)
    meta: Dict = {}
    body = text
    if fm_match:
        fm_text = fm_match.group(1)
        body = text[fm_match.end() :]
        # Best-effort parse of simple YAML k: v pairs (no nesting)
        for line in fm_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta, body.strip()


def safe_load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def safe_write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def sentence_lengths(text: str) -> List[int]:
    # Split by common Chinese punctuation and periods
    parts = re.split(r"[。？！!？;；\n]+", text)
    lens = [len(p.strip()) for p in parts if p.strip()]
    return lens


def sentence_length_buckets(lengths: List[int]) -> Dict[str, int]:
    buckets = {"1-10": 0, "11-20": 0, "21-30": 0, "30+": 0}
    for l in lengths:
        if l <= 10:
            buckets["1-10"] += 1
        elif l <= 20:
            buckets["11-20"] += 1
        elif l <= 30:
            buckets["21-30"] += 1
        else:
            buckets["30+"] += 1
    return buckets


def build_cooccurrence(concepts: List[str], window: int = 50) -> List[Tuple[str, str, int]]:
    # Simple fully-connected cooccurrence weighted by shared rank
    # Assumes `concepts` already top-ranked; use index distance as proxy weight
    edges: Dict[Tuple[str, str], int] = {}
    for i, a in enumerate(concepts):
        for j in range(i + 1, min(len(concepts), i + window)):
            b = concepts[j]
            key = (a, b) if a < b else (b, a)
            edges[key] = edges.get(key, 0) + (window - (j - i))
    return [(a, b, w) for (a, b), w in edges.items()]


def retry_request(max_retries: int = 3, backoff_base: float = 0.8):
    import logging
    
    def deco(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get logger from the function's module, not from utils
            logger = logging.getLogger(func.__module__)
            last_exc = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # noqa: BLE001
                    last_exc = e
                    sleep_s = (backoff_base ** attempt) * 2.0
                    if attempt < max_retries - 1:
                        logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}), retrying in {sleep_s:.1f}s: {e}")
                    time.sleep(min(8.0, max(0.5, sleep_s)))
            if last_exc:
                logger.error(f"Request failed after {max_retries} attempts: {last_exc}")
                raise last_exc
        return wrapper
    return deco


