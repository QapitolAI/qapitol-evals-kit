from __future__ import annotations

import asyncio
from typing import Any

from qapitol.evals.base import BaseEvaluator
from qapitol.evals.score import Score


async def evaluate_batch(
    evaluator: BaseEvaluator,
    records: list[dict[str, Any]],
    *,
    concurrency: int = 4,
) -> list[Score]:
    """Evaluate multiple records concurrently."""
    sem = asyncio.Semaphore(concurrency)

    async def _one(record: dict[str, Any]) -> Score:
        async with sem:
            return await evaluator.async_evaluate(record)

    return await asyncio.gather(*[_one(r) for r in records])


def evaluate_batch_sync(
    evaluator: BaseEvaluator,
    records: list[dict[str, Any]],
    *,
    concurrency: int = 4,
) -> list[Score]:
    return asyncio.run(evaluate_batch(evaluator, records, concurrency=concurrency))
