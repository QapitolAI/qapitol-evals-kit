from __future__ import annotations

import json


class MockCompletionClient:
    """Deterministic LLM completions for unit tests."""

    def __init__(self, responses: dict[str, str] | None = None) -> None:
        self.responses = responses or {}
        self.calls: list[str] = []

    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        for key, value in self.responses.items():
            if key in prompt:
                return value
        return json.dumps(
            {"score": 0.9, "label": "pass", "explanation": "mock judge"},
        )
