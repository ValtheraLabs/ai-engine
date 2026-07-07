import json
from typing import Any

import httpx

from app.core.config import settings


class LLMUnavailableError(Exception):
    pass


def _ollama_generate(prompt: str) -> str:
    url = f"{settings.ollama_base_url}/api/generate"
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    try:
        response = httpx.post(
            url,
            json=payload,
            timeout=settings.ollama_timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError) as exc:
        raise LLMUnavailableError(str(exc)) from exc


def analyze_with_llm(prompt: str) -> dict[str, Any] | None:
    try:
        raw = _ollama_generate(prompt)
        return json.loads(raw)
    except (LLMUnavailableError, json.JSONDecodeError):
        return None
