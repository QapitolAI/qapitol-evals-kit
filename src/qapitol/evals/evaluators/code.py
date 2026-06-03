from __future__ import annotations

import re
from typing import Any

from qapitol.evals.base import BaseEvaluator
from qapitol.evals.score import Score


def _normalize(text: str, *, case_sensitive: bool, strip: bool) -> str:
    value = text
    if strip:
        value = value.strip()
    if not case_sensitive:
        value = value.lower()
    return value


class ExactMatchEvaluator(BaseEvaluator):
    """Binary match between output and expected."""

    name = "exact_match"

    def __init__(
        self,
        *,
        case_sensitive: bool = True,
        strip: bool = True,
    ) -> None:
        self.case_sensitive = case_sensitive
        self.strip = strip

    def evaluate(self, record: dict[str, Any]) -> Score:
        self._require_fields(record, ["output", "expected"])
        out = _normalize(
            str(record["output"]),
            case_sensitive=self.case_sensitive,
            strip=self.strip,
        )
        exp = _normalize(
            str(record["expected"]),
            case_sensitive=self.case_sensitive,
            strip=self.strip,
        )
        match = out == exp
        return Score(
            score=1.0 if match else 0.0,
            name=self.name,
            label="match" if match else "mismatch",
            explanation="Output matches expected." if match else "Output does not match expected.",
            kind="code",
            direction="maximize",
        )


class CustomAccuracyEvaluator(BaseEvaluator):
    """Flexible accuracy with optional regex or normalized substring match."""

    name = "custom_accuracy"

    def __init__(
        self,
        *,
        mode: str = "contains",
        case_sensitive: bool = False,
        strip: bool = True,
    ) -> None:
        if mode not in ("contains", "regex", "equal"):
            raise ValueError("mode must be one of: contains, regex, equal")
        self.mode = mode
        self.case_sensitive = case_sensitive
        self.strip = strip

    def evaluate(self, record: dict[str, Any]) -> Score:
        self._require_fields(record, ["output", "expected"])
        out = _normalize(
            str(record["output"]),
            case_sensitive=self.case_sensitive,
            strip=self.strip,
        )
        exp = _normalize(
            str(record["expected"]),
            case_sensitive=self.case_sensitive,
            strip=self.strip,
        )
        if self.mode == "equal":
            ok = out == exp
        elif self.mode == "contains":
            ok = exp in out
        else:
            ok = bool(re.search(exp, out))
        return Score(
            score=1.0 if ok else 0.0,
            name=self.name,
            label="accurate" if ok else "inaccurate",
            explanation=f"Accuracy check ({self.mode}) {'passed' if ok else 'failed'}.",
            kind="code",
            direction="maximize",
            metadata={"mode": self.mode},
        )
