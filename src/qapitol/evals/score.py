from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

ScoreKind = Literal["code", "llm"]
ScoreDirection = Literal["maximize", "minimize"]


class Score(BaseModel):
    """Standard result from any evaluator."""

    score: float = Field(ge=0.0, le=1.0)
    name: str
    label: str
    explanation: str = ""
    kind: ScoreKind
    direction: ScoreDirection = "maximize"
    metadata: dict[str, Any] = Field(default_factory=dict)

    def passed_threshold(self, threshold: float) -> bool:
        if self.direction == "maximize":
            return self.score >= threshold
        return self.score <= threshold
