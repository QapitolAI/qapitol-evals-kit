from __future__ import annotations

from typing import Any

from qapitol.evals.base import BaseEvaluator
from qapitol.evals.batch import evaluate_batch_sync
from qapitol.evals.score import Score


def run_metrics(
    records: list[dict[str, Any]],
    evaluators: list[BaseEvaluator],
    *,
    concurrency: int = 4,
) -> list[dict[str, Any]]:
    """Run multiple evaluators over the same records; attach scores to each row."""
    if not evaluators:
        return [dict(r) for r in records]

    scores_by_evaluator = [
        evaluate_batch_sync(ev, records, concurrency=concurrency) for ev in evaluators
    ]
    results: list[dict[str, Any]] = []
    for i, record in enumerate(records):
        row = dict(record)
        row["scores"] = [scores_by_evaluator[j][i] for j in range(len(evaluators))]
        results.append(row)
    return results


def summarize(scores_by_metric: dict[str, list[Score]]) -> dict[str, float]:
    """Return mean score per metric name."""
    return {
        name: sum(s.score for s in scores) / len(scores)
        for name, scores in scores_by_metric.items()
        if scores
    }
