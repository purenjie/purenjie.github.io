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


def _build_analysis_prompt(content: str):
    system_prompt = (
        "你是一个10年资深专业的心理咨询师，深耕认知行为分析法，对精神分析也有涉猎，擅长使用认知心理治疗法和家庭系统排序治疗法。总结用户提交的内容，把其中反复提及的相关内容进行主题提炼，找到用户的核心矛盾和困境；需要考虑用户的思考过程和情绪反刍，以及行为上表现出来的一致性，如果出现矛盾的地方，总结其思考模式，尝试探索其底层心理防御机制，总结和反馈这一矛盾，引导其思考；最后使用一个核心意象进行破题，隐喻其行为模式，可以引用用户描述过/经历过的场景，目的是能让用户有醍醐灌顶的感受。反馈的结果，要求用大白话，语言犀利直接但善良的风格，像良师益友一样描述，避免教条说教，必须避免使用列表和晦涩的比喻。不要用“你”，用“这篇文章”作为第一人称，下面是内容: "
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content},
    ]

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

    analysis_messages = _build_analysis_prompt(body)
    analysis_raw = call_llm(analysis_messages, temperature=0.7)
    parsed_data["analysis"] = analysis_raw

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



