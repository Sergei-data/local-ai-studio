from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str = "deepseek-coder-v2:lite") -> None:
        self.base_url = base_url or settings.ollama_base_url
        self.model = model

    async def generate(self, prompt: str, model: str | None = None, system: str | None = None) -> str:
        payload: dict[str, Any] = {
            "model": model or self.model,
            "prompt": prompt,
            "stream": False,
        }

        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()

        text = data.get("response", "")
        if not isinstance(text, str):
            raise ValueError("Invalid Ollama response format")

        return text.strip()