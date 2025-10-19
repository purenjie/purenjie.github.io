"""AI analysis package for blog content.

This package provides a two-stage (Map-Reduce) analysis pipeline:
1) Map: Analyze each article into a structured JSON.
2) Reduce: Aggregate all article analyses into a global summary JSON.

Notes:
- Comments are in English as required.
- LLM calls follow the same authentication style as generate_cover_image.py.
"""

__all__ = [
    "config",
    "schema",
    "utils",
    "llm",
    "map_analyze",
    "reduce_analyze",
]


