"""LLM client wrapper for Ark (Volcengine) compatible API.

This mirrors the authentication style used in generate_cover_image.py.
"""

from __future__ import annotations

import json
import logging
from typing import List, Literal, Optional

import requests

from .config import BASE_URL, API_KEY, REQUEST_TIMEOUT_S, TEXT_MODEL
from .utils import retry_request

logger = logging.getLogger(__name__)

Role = Literal["system", "user", "assistant"]


class LlmError(Exception):
    pass


@retry_request()
def call_llm(
    messages: List[dict],
    model: Optional[str] = None,
    temperature: float = 0.7,
) -> str:
    if not API_KEY:
        raise LlmError("API_KEY not set in environment")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    data = {
        "model": model or TEXT_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    logger.debug(f"LLM call: model={model or TEXT_MODEL}")
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data,
        timeout=REQUEST_TIMEOUT_S,
    )
    resp.raise_for_status()
    result = resp.json()
    
    try:
        content = result["choices"][0]["message"]["content"].strip()
        finish_reason = result["choices"][0].get("finish_reason")
        
        # Extract JSON from markdown code blocks if present
        if content.startswith("```"):
            logger.debug("Removing markdown code block markers")
            lines = content.split("\n")
            # Remove first line if it starts with ```
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            # Remove last line if it's just ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines).strip()
        
        logger.debug(f"LLM response: {len(content)} chars, finish_reason={finish_reason}")
        if finish_reason == "length":
            logger.warning("LLM response was truncated (finish_reason=length)")
        
        return content
    except Exception as e:  # noqa: BLE001
        raise LlmError(f"Unexpected LLM response: {json.dumps(result)[:500]}") from e


