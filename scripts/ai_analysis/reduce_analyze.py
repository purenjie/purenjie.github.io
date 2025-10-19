"""Reduce stage: aggregate article analyses into global summary.

Combines statistical signals (TF-IDF/KMeans draft, cooccurrence) with LLM
to produce human-friendly topic naming and high-level interpretations.
"""

from __future__ import annotations

import json
import logging
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

from .config import NUM_TOPICS
from .llm import call_llm
from .schema import ArticleAnalysis, ConceptLink, ConceptNode, GlobalAnalysis, StructureItem, Summary, TopicItem

logger = logging.getLogger(__name__)


def _draft_topics(articles: List[ArticleAnalysis]) -> List[Tuple[str, float]]:
    # Simple frequency-based draft: use top tags/keywords as topic hints
    pool: Counter[str] = Counter()
    for a in articles:
        for t in a.tags:
            if t:
                pool[t] += 1
        for k in a.content.keywords:
            if k:
                pool[k] += 1
    total = sum(pool.values()) or 1
    top = pool.most_common(NUM_TOPICS)
    return [(w, c / total) for w, c in top]


def _concept_network(articles: List[ArticleAnalysis]) -> Dict[str, List[Dict]]:
    node_weight: Counter[str] = Counter()
    link_weight: Counter[Tuple[str, str]] = Counter()
    for a in articles:
        concepts = [c for c in a.content.concepts if c]
        for i, s in enumerate(concepts):
            node_weight[s] += 1
            for j in range(i + 1, min(len(concepts), i + 10)):
                t = concepts[j]
                key = (s, t) if s < t else (t, s)
                link_weight[key] += 1
    nodes = [ConceptNode(id=k, weight=v).dict() for k, v in node_weight.items()]
    links = [
        {"source": s, "target": t, "weight": w} for (s, t), w in link_weight.items()
    ]
    return {"nodes": nodes, "links": links}


def _calculate_tone_avg(articles: List[ArticleAnalysis]) -> Dict[str, float]:
    """Calculate average tone across all articles."""
    tone_keys = ["teaching", "reflective", "humor", "critical"]
    tone_sums: Dict[str, float] = defaultdict(float)
    tone_counts: Dict[str, int] = defaultdict(int)
    
    for a in articles:
        for key in tone_keys:
            val = a.style.tone.get(key)
            if val is not None:
                tone_sums[key] += val
                tone_counts[key] += 1
    
    return {k: round(tone_sums[k] / tone_counts[k], 2) if tone_counts[k] > 0 else 0.0 
            for k in tone_keys}


def _calculate_sentiment_dist(articles: List[ArticleAnalysis]) -> Dict[str, float]:
    """Calculate sentiment distribution across all articles."""
    sentiment_map = {
        "positive": ["积极", "积极反思", "积极向上", "理性积极", "积极指导"],
        "neutral": ["中性", "中性偏", "中性技术说明", "反思性中立", "中性偏技术"],
        "negative": ["消极", "负面"]
    }
    
    counts = {"positive": 0, "neutral": 0, "negative": 0}
    total = 0
    
    for a in articles:
        label = a.sentiment.label
        if not label:
            continue
        total += 1
        
        # Fuzzy matching for sentiment labels
        categorized = False
        for category, keywords in sentiment_map.items():
            if any(kw in label for kw in keywords):
                counts[category] += 1
                categorized = True
                break
        
        # Default to neutral if no match
        if not categorized:
            counts["neutral"] += 1
    
    if total == 0:
        return {"positive": 0.0, "neutral": 0.0, "negative": 0.0}
    
    return {k: round(v / total, 3) for k, v in counts.items()}


def _calculate_timeline_depth(articles: List[ArticleAnalysis]) -> List[Dict[str, str]]:
    """Build timeline of article depth by date."""
    timeline = []
    for a in articles:
        if a.date and a.depth:
            timeline.append({"date": a.date, "depth": a.depth})
    
    # Sort by date
    timeline.sort(key=lambda x: x["date"] if x["date"] else "")
    return timeline


def _calculate_structures(articles: List[ArticleAnalysis]) -> List[StructureItem]:
    """Count structure patterns."""
    pattern_counts: Counter[str] = Counter()
    for a in articles:
        pattern = a.structure.pattern
        if pattern:
            pattern_counts[pattern] += 1
    
    return [StructureItem(pattern=p, count=c) for p, c in pattern_counts.most_common()]


def _build_reduce_prompt(articles: List[ArticleAnalysis], draft_topics: List[Tuple[str, float]]):
    """Build LLM prompt for topic naming (optional enhancement)."""
    system_prompt = (
        "你是一位负责整合多篇文章分析的高级编辑。根据提供的草拟主题，为这些主题命名（3-5个主题）并给出每个主题的代表性文章。"
        "返回严格的JSON格式：{\"topics\": [{\"name\": \"主题名\", \"ratio\": 0.x, \"representatives\": [\"文章标题\"]}]}"
    )
    light_articles = [
        {
            "id": a.id,
            "title": a.title,
            "tags": a.tags[:3],  # Only top 3 tags
            "keywords": a.content.keywords[:5],  # Only top 5 keywords
        }
        for a in articles
    ]
    user_payload = {
        "articles": light_articles[:20],  # Sample only 20 articles to reduce token usage
        "draft_topics": draft_topics,
        "num_topics": NUM_TOPICS
    }
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
    ]
    return messages


def reduce_global(articles: List[ArticleAnalysis]) -> GlobalAnalysis:
    """Reduce all articles into global summary with statistics."""
    logger.info(f"Starting global analysis reduction for {len(articles)} articles")
    
    # Calculate all statistics directly via code
    tone_avg = _calculate_tone_avg(articles)
    logger.debug(f"Calculated tone averages: {tone_avg}")
    
    avg_sentence = 0.0
    lens = [a.metrics.sentenceAvgLen for a in articles if a.metrics.sentenceAvgLen]
    if lens:
        avg_sentence = round(sum(lens) / len(lens), 2)
    
    sentiment_dist = _calculate_sentiment_dist(articles)
    logger.debug(f"Calculated sentiment distribution: {sentiment_dist}")
    
    concept_network = _concept_network(articles)
    logger.debug(f"Built concept network: {len(concept_network.get('nodes', []))} nodes")
    
    timeline_depth = _calculate_timeline_depth(articles)
    structures = _calculate_structures(articles)
    
    # Optional: Use LLM for topic naming (can be skipped for speed)
    draft_topics = _draft_topics(articles)
    topics: List[TopicItem] = []
    try:
        messages = _build_reduce_prompt(articles, draft_topics)
        raw = call_llm(messages, temperature=0.5)
        parsed = json.loads(raw)
        topics = [TopicItem(**t) for t in parsed.get("topics", []) if isinstance(t, dict)]
        logger.info(f"LLM generated {len(topics)} named topics")
    except Exception as e:
        logger.warning(f"Failed to get LLM topic naming, using draft topics: {e}")
        # Fallback to draft topics
        topics = [
            TopicItem(name=name, ratio=ratio, representatives=[])
            for name, ratio in draft_topics
        ]
    
    summary = Summary(
        style={"toneAvg": tone_avg},
        avgSentenceLen=avg_sentence,
        sentimentDist=sentiment_dist,
        topics=topics,
        conceptNetwork=concept_network,
        timelineDepth=timeline_depth,
        structures=structures,
        topicSentiment=[],  # Can be calculated later if needed
    )

    logger.info("✅ Global summary calculation complete")
    return GlobalAnalysis(summary=summary, perArticle=articles)


