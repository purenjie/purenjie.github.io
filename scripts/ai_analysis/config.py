"""Configuration for AI analysis pipeline.

All constants are centralized here to simplify maintenance.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional



BASE_URL: str = "https://api.deepseek.com/v1"
TEXT_MODEL: str = "deepseek-chat"

# API Key (required). Keep the same variable name for consistency
API_KEY: Optional[str] = os.getenv("API_KEY")

# Timeouts and retry settings
REQUEST_TIMEOUT_S: int = int(os.getenv("AI_REQUEST_TIMEOUT_S", "500"))
MAX_RETRIES: int = int(os.getenv("AI_MAX_RETRIES", "3"))

# IO paths (adjusted for location under project_root/scripts/ai_analysis)
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # .../blog
CONTENT_BLOG_DIR = PROJECT_ROOT / "src" / "content" / "blog"

AI_DIR = PROJECT_ROOT / "scripts" / "ai_analysis"
CACHE_DIR = AI_DIR / "cache"
MANIFEST_PATH = AI_DIR / "manifest.json"

PUBLIC_DATA_DIR = PROJECT_ROOT / "public" / "data"
OUTPUT_GLOBAL = PUBLIC_DATA_DIR / "blog-analysis.json"

# Clustering parameters
NUM_TOPICS = int(os.getenv("AI_NUM_TOPICS", "4"))  # 3-5 recommended

# Ensure directories exist at import time (safe operation)
for p in (CACHE_DIR, PUBLIC_DATA_DIR):
    try:
        p.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Do not crash on import; creation will be attempted again on run
        pass


