from __future__ import annotations

import json
import os
import re
from typing import Any, Protocol


class CompletionClient(Protocol):
    """Protocol for test doubles and provider backends."""

    def complete(self, prompt: str) -> str:
        ...


class LLM:
    """BYOK LLM wrapper for judge calls."""

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        *,
        client: CompletionClient | None = None,
        temperature: float = 0.0,
    ) -> None:
        self.provider = provider.lower()
        self.model = model
        self.temperature = temperature
        self._client = client

    def complete(self, prompt: str) -> str:
        if self._client is not None:
            return self._client.complete(prompt)
        if self.provider == "openai":
            return self._complete_openai(prompt)
        if self.provider == "anthropic":
            return self._complete_anthropic(prompt)
        raise ValueError(f"Unsupported provider: {self.provider}")

    def _complete_openai(self, prompt: str) -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        try:
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError("Install openai: pip install qapitol-evals-kit[openai]") from e
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        return response.choices[0].message.content or ""

    def _complete_anthropic(self, prompt: str) -> str:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise RuntimeError(
                "Install anthropic: pip install qapitol-evals-kit[anthropic]"
            ) from e
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        parts = [block.text for block in response.content if hasattr(block, "text")]
        return "".join(parts)


def parse_judge_json(text: str) -> dict[str, Any]:
    """Extract JSON object from model response."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse judge JSON from: {text[:200]}") from None
        return json.loads(match.group())
