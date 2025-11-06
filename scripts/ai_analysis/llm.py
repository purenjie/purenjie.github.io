"""LLM client wrapper for Ark (Volcengine) compatible API.

This mirrors the authentication style used in generate_cover_image.py.
"""

from __future__ import annotations

import json
import logging
import re
from typing import List, Literal, Optional

import requests

from .config import BASE_URL, API_KEY, REQUEST_TIMEOUT_S, TEXT_MODEL
from .utils import retry_request

logger = logging.getLogger(__name__)

Role = Literal["system", "user", "assistant"]


def clean_and_validate_json(content: str) -> str:
    """
    Clean and validate JSON response from LLM.

    This function attempts to fix common LLM JSON formatting errors:
    - Missing colon after keys
    - Unquoted keys
    - Trailing commas
    - Extra whitespace

    Returns the cleaned JSON string or the original if it can't be fixed.
    """
    if not content:
        return content

    # Remove markdown code blocks if present
    if content.startswith("```"):
        lines = content.split("\n")
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines).strip()

    # Track original for logging
    original_content = content

    # Common LLM JSON fixes
    fixes = [
        # Fix missing colon after key (e.g., "tropes [" -> "tropes": [)
        (r'(\w+)\s+\[', r'"\1": ['),
        (r'(\w+)\s+\{', r'"\1": {'),
        (r'(\w+)\s*"', r'"\1": "'),
        (r'(\w+)\s*\'', r'"\1": \''),
        # Fix unquoted keys (add quotes if followed by colon)
        (r'(\w+):', r'"\1":'),
        # Fix trailing commas in objects/arrays
        (r',(\s*[}\]])', r'\1'),
        # Fix missing commas between array/object elements
        (r'}\s*{', r'}, {'),
        (r']\s*\[', r'], ['),
        (r'"\s*}', r'", }'),
        (r'"\s*]', r'", ]'),
    ]

    # Apply fixes
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content)

    # Validate JSON
    try:
        json.loads(content)
        if content != original_content:
            logger.debug(f"JSON cleaned successfully: {len(original_content)} -> {len(content)} chars")
        return content
    except json.JSONDecodeError as e:
        logger.debug(f"JSON validation failed after cleaning: {e}")
        # Try to save the problematic part for debugging
        error_pos = getattr(e, 'pos', 0)
        if error_pos > 0:
            start = max(0, error_pos - 50)
            end = min(len(content), error_pos + 50)
            logger.debug(f"Error near position {error_pos}: {content[start:end]}")
        return original_content  # Return original for fallback handling


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

    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data,
        timeout=REQUEST_TIMEOUT_S,
    )
    resp.raise_for_status()
    result = resp.json()
    logger.debug(f"LLM call: model={model or TEXT_MODEL}, messages={messages}, result={resp.text}")
    
    try:
        content = result["choices"][0]["message"]["content"].strip()
        finish_reason = result["choices"][0].get("finish_reason")

        # Clean and validate JSON
        content = clean_and_validate_json(content)

        logger.debug(f"LLM response: {content}, finish_reason={finish_reason}")
        if finish_reason == "length":
            logger.warning("LLM response was truncated (finish_reason=length)")

        return content
    except Exception as e:  # noqa: BLE001
        raise LlmError(f"Unexpected LLM response: {json.dumps(result)[:500]}") from e


