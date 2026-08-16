"""LLM client wrapper using OpenRouter."""

from __future__ import annotations

import json
import logging

from openai import AsyncOpenAI  # pyrefly: ignore [missing-import]

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)

logger = logging.getLogger(__name__)


def _build_client() -> AsyncOpenAI:
    """Construct the OpenRouter async client."""
    logger.info("Using OpenRouter API")
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )


_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = _build_client()
    return _client


def reset_client() -> None:
    """Reset the client."""
    global _client
    _client = None


async def chat_completion(
    system_prompt: str,
    user_message: str,
    *,
    temperature: float = 0.3,
    response_format: dict | None = None,
) -> str:
    """Send a chat completion request and return the assistant message text."""
    client = get_client()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    kwargs: dict = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "temperature": temperature,
    }
    if response_format:
        kwargs["response_format"] = response_format

    resp = await client.chat.completions.create(**kwargs)
    content = resp.choices[0].message.content or ""
    logger.debug("LLM response: %s", content[:500])
    return content

async def chat_completion_json(
    system_prompt: str,
    user_message: str,
    *,
    temperature: float = 0.2,
) -> dict:
    """Chat completion that returns parsed JSON."""
    raw = await chat_completion(
        system_prompt,
        user_message,
        temperature=temperature,
        response_format={"type": "json_object"},
    )

    raw = raw.strip()

    logger.info("Raw JSON response: %r", raw[:2000])

    # Remove Markdown code fences if the model added them
    if raw.startswith("```"):
        lines = raw.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        raw = "\n".join(lines).strip()

    if not raw:
        raise ValueError(
            "LLM returned an empty response when JSON was expected."
        )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON returned by LLM: %r", raw[:5000])
        raise ValueError(
            f"LLM returned invalid JSON: {raw[:1000]}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(
            f"Expected JSON object, got {type(data).__name__}"
        )

    return data