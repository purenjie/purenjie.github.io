"""Map stage: analyze a single article to structured JSON using LLM + jieba.

Steps:
1) Parse frontmatter and body
2) Compute MD5 for cache key
3) Extract basic metrics (sentence lengths, readability proxies)
4) Use jieba for top words as hints
5) Prompt LLM to produce structured JSON (ArticleAnalysis)
6) Validate with pydantic, fallback to minimal structure on failure
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List

from .llm import call_llm
from .schema import ArticleAnalysis
from .utils import (
    md5_hash_text,
    parse_frontmatter_and_body,
    sentence_length_buckets,
    sentence_lengths,
)

logger = logging.getLogger(__name__)


def _build_map_prompt(meta: Dict, content: str, schema_hint: Dict) -> List[dict]:
    system_prompt = (
        "你是一个精确的文学和技术风格分析师。 给定一个中文博客文章块和元数据，生成符合模式的严格的 JSON。 不要包含解释。只输出 JSON，回复内容必须使用中文。下面是我的内容: "
    )
    user_payload = {
        "meta": meta,
        "content": content,
        "json_schema_hint": schema_hint,
    }
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
    ]


def analyze_single_article(path: Path) -> ArticleAnalysis:
    logger.info(f"Analyzing article: {path.name}")
    meta, body = parse_frontmatter_and_body(path)
    article_id = path.stem
    title = meta.get("title", article_id)
    date = meta.get("pubDate") or meta.get("date")
    tags = []
    if meta.get("tags"):
        # naive split for simple frontmatter lists
        tags = [t.strip().strip("- ") for t in str(meta["tags"]).split("\n") if t.strip()]

    content_md5 = md5_hash_text(body)

    lens = sentence_lengths(body)
    avg_len = round(sum(lens) / max(1, len(lens)), 2) if lens else 0.0
    buckets = sentence_length_buckets(lens)

    schema_hint = {
        "id": "str",
        "title": "str",
        "date": "str",
        "tags": ["str"],
        "slug": "str",
        "path": "str",
        "md5": "str",
        "metrics": {
            "sentenceAvgLen": "float",
            "sentenceLenBuckets": {"1-10": "int", "11-20": "int", "21-30": "int", "30+": "int"},
            "readability": {"chars": "int", "words": "int", "paragraphs": "int"},
        },
        "style": {"tone": {"teaching": "float", "reflective": "float", "humor": "float", "critical": "float"}, "rhythm": "str", "tropes": ["str"]},
        "content": {"keywords": ["str"], "concepts": ["str"]},
        "sentiment": {"label": "str", "score": "float"},
        "structure": {"pattern": "str", "opening": "str", "closing": "str"},
        "depth": "str",
    }

    messages = _build_map_prompt(
        {
            "id": article_id,
            "title": title,
            "date": date,
            "tags": tags,
            "path": str(path),
        },
        body,
        schema_hint,
    )
    raw = call_llm(messages, temperature=0.5)
    
    # Parse LLM response
    try:
        parsed_data = json.loads(raw)
    except Exception as e:
        logger.warning(f"Failed to parse LLM JSON: {e} {raw}")
        # Fallback to minimal data
        parsed_data = {}

    # Fill required fields with defaults
    parsed_data.setdefault("id", article_id)
    parsed_data.setdefault("title", title)
    parsed_data.setdefault("date", date)
    parsed_data.setdefault("tags", tags)
    parsed_data.setdefault("slug", article_id)
    parsed_data.setdefault("path", str(path))
    parsed_data["md5"] = content_md5
    
    # Fill metrics if missing
    if "metrics" not in parsed_data or not parsed_data["metrics"]:
        parsed_data["metrics"] = {}
    parsed_data["metrics"].setdefault("sentenceAvgLen", avg_len)
    parsed_data["metrics"].setdefault("sentenceLenBuckets", buckets)
    parsed_data["metrics"].setdefault("readability", {
        "chars": len(body), 
        "words": len(body), 
        "paragraphs": len(body.splitlines())
    })


    result = ArticleAnalysis(**parsed_data)
    logger.info(f"Successfully analyzed: {title}")
    return result



