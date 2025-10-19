"""CLI entry: scan blog posts, map-reduce analysis with MD5 caching.

Usage:
  python -m scripts.ai_analysis.run [--force] [--limit N] [--verbose] [--dry-run]
  or
  python scripts/ai_analysis/run.py [--force] [--limit N] [--verbose] [--dry-run]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

# Support both direct script execution and module execution
if __name__ == "__main__" and __package__ is None:
    # Add parent directory to path for direct script execution
    _script_dir = Path(__file__).resolve().parent
    _parent_dir = _script_dir.parent
    if str(_parent_dir) not in sys.path:
        sys.path.insert(0, str(_parent_dir))
    __package__ = "ai_analysis"

from .config import CACHE_DIR, CONTENT_BLOG_DIR, MANIFEST_PATH, OUTPUT_GLOBAL
from .reduce_analyze import reduce_global
from .schema import ArticleAnalysis
from .utils import md5_hash_text, parse_frontmatter_and_body, safe_load_json, safe_write_json
from .map_analyze import analyze_single_article

# Logger will be configured in main()
logger = logging.getLogger(__name__)


def _article_candidates() -> List[Path]:
    paths: List[Path] = []
    for p in CONTENT_BLOG_DIR.glob("**/*.md"):
        if p.name.lower() == "index.md" or p.suffix.lower() == ".md":
            paths.append(p)
    return sorted(paths)


def _safe_article_name(article_path: Path) -> str:
    return article_path.parent.name if article_path.name.lower() == "index.md" else article_path.stem


def _cache_filename(article_path: Path, body_md5: str) -> Path:
    safe_name = _safe_article_name(article_path)
    return CACHE_DIR / f"{safe_name}_{body_md5}.json"


def main():
    parser = argparse.ArgumentParser(description="AI analysis for blog posts")
    parser.add_argument("--force", action="store_true", help="recompute and ignore cache")
    parser.add_argument("--limit", type=int, default=0, help="limit number of articles")
    parser.add_argument("--verbose", action="store_true", help="verbose logging")
    parser.add_argument("--dry-run", action="store_true", help="no LLM calls, only list targets")
    args = parser.parse_args()

    # Setup logging - configure root logger and all handlers
    log_level = logging.DEBUG if args.verbose else logging.INFO
    
    # Clear any existing handlers to ensure fresh configuration
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    
    # Ensure our module loggers use the root logger's configuration
    logging.getLogger("ai_analysis").setLevel(log_level)
    logging.getLogger("scripts.ai_analysis").setLevel(log_level)

    candidates = _article_candidates()
    logger.info(f"Found {len(candidates)} articles in {CONTENT_BLOG_DIR}")
    
    if args.limit > 0:
        candidates = candidates[: args.limit]
        logger.info(f"Limited to {args.limit} articles")

    manifest = safe_load_json(MANIFEST_PATH) or {"latest": {}, "history": []}

    tasks: List[Path] = []
    for ap in candidates:
        _, body = parse_frontmatter_and_body(ap)
        h = md5_hash_text(body)
        cache_file = _cache_filename(ap, h)
        if args.force:
            tasks.append(ap)
        else:
            if cache_file.exists():
                logger.debug(f"Cache hit: {ap.name}")
                # Record latest mapping
                manifest["latest"][str(ap)] = cache_file.name
                continue
            tasks.append(ap)

    logger.info(f"Processing {len(tasks)} articles ({len(candidates) - len(tasks)} cached)")

    if args.dry_run:
        for t in tasks:
            logger.info(f"DRY RUN target: {t}")
        return

    results: List[ArticleAnalysis] = []

    def _work(p: Path) -> Optional[ArticleAnalysis]:
        try:
            analysis = analyze_single_article(p)
            # Write cache
            cache_path = _cache_filename(p, analysis.md5)
            safe_write_json(cache_path, analysis.model_dump())
            return analysis
        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to analyze {p.name}: {e}")
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(_work, tasks):
            if res is not None:
                results.append(res)
                ap = Path(res.path)
                manifest["latest"][str(ap)] = f"{_safe_article_name(ap)}_{res.md5}.json"
                manifest["history"].append({"path": res.path, "md5": res.md5})
    
    logger.info(f"Successfully analyzed {len(results)}/{len(tasks)} new articles")

    # Load latest from cache for all candidates to build full perArticle list
    per_article: List[ArticleAnalysis] = []
    for ap in candidates:
        entry = manifest["latest"].get(str(ap))
        if not entry:
            continue
        cf = CACHE_DIR / entry
        js = safe_load_json(cf)
        if js:
            try:
                per_article.append(ArticleAnalysis(**js))
            except Exception as e:
                logger.warning(f"Failed to load cached analysis for {ap.name}: {e}")

    logger.info(f"Loaded {len(per_article)} total articles for global reduction")
    global_js = reduce_global(per_article)
    safe_write_json(OUTPUT_GLOBAL, global_js.model_dump())
    safe_write_json(MANIFEST_PATH, manifest)
    logger.info(f"✅ Global analysis written to: {OUTPUT_GLOBAL}")


if __name__ == "__main__":
    main()


