"""Data schemas for article-level and global analysis outputs.

Pydantic is used to validate and ensure consistent outputs.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class Metrics(BaseModel):
    sentenceAvgLen: float = 0.0
    sentenceLenBuckets: Dict[str, int] = Field(default_factory=dict)
    readability: Dict[str, Union[int, float]] = Field(default_factory=dict)


class Style(BaseModel):
    tone: Dict[str, float] = Field(default_factory=dict)
    rhythm: Optional[str] = None
    tropes: List[str] = Field(default_factory=list)


class ContentInfo(BaseModel):
    keywords: List[str] = Field(default_factory=list)
    concepts: List[str] = Field(default_factory=list)


class Sentiment(BaseModel):
    label: Optional[str] = None
    score: Optional[float] = None


class Structure(BaseModel):
    pattern: Optional[str] = None
    opening: Optional[str] = None
    closing: Optional[str] = None


class Diagnostics(BaseModel):
    llm_raw: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)


class ArticleAnalysis(BaseModel):
    id: str
    title: str
    date: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    slug: Optional[str] = None
    path: str
    md5: str

    metrics: Metrics = Field(default_factory=Metrics)
    style: Style = Field(default_factory=Style)
    content: ContentInfo = Field(default_factory=ContentInfo)
    sentiment: Sentiment = Field(default_factory=Sentiment)
    stance: Dict[str, Optional[str]] = Field(default_factory=dict)
    structure: Structure = Field(default_factory=Structure)
    depth: Optional[str] = None

    diagnostics: Diagnostics = Field(default_factory=Diagnostics)


class ConceptNode(BaseModel):
    id: str
    weight: int


class ConceptLink(BaseModel):
    source: str
    target: str
    weight: int


class TopicItem(BaseModel):
    name: str
    ratio: float
    representatives: List[str] = Field(default_factory=list)


class TopicSentiment(BaseModel):
    topic: str
    positive: float
    neutral: float
    negative: float


class StructureItem(BaseModel):
    pattern: str
    count: int


class Summary(BaseModel):
    style: Dict[str, Dict[str, float]] = Field(default_factory=dict)  # {toneAvg: {...}}
    avgSentenceLen: Optional[float] = None
    sentimentDist: Dict[str, float] = Field(default_factory=dict)
    topics: List[TopicItem] = Field(default_factory=list)
    conceptNetwork: Dict[str, List[Dict]] = Field(default_factory=dict)  # nodes/links
    timelineDepth: List[Dict[str, str]] = Field(default_factory=list)
    structures: List[StructureItem] = Field(default_factory=list)
    topicSentiment: List[TopicSentiment] = Field(default_factory=list)


class GlobalAnalysis(BaseModel):
    summary: Summary
    perArticle: List[ArticleAnalysis]


