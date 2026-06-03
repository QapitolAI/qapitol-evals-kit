from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from qapitol.evals.score import Score


class BaseEvaluator(ABC):
    """Base class for all evaluators."""

    name: str = "base"

    @abstractmethod
    def evaluate(self, record: dict[str, Any]) -> Score:
        """Evaluate a single record synchronously."""

    async def async_evaluate(self, record: dict[str, Any]) -> Score:
        """Default async wrapper around sync evaluate."""
        return self.evaluate(record)

    def _require_fields(self, record: dict[str, Any], fields: list[str]) -> None:
        missing = [f for f in fields if f not in record or record[f] is None]
        if missing:
            raise ValueError(f"{self.name} requires fields: {', '.join(missing)}")
