import pytest

from qapitol.evals.batch import evaluate_batch, evaluate_batch_sync
from qapitol.evals.evaluators.code import ExactMatchEvaluator


@pytest.mark.asyncio
async def test_evaluate_batch_async() -> None:
    ev = ExactMatchEvaluator()
    records = [
        {"output": "a", "expected": "a"},
        {"output": "b", "expected": "c"},
    ]
    scores = await evaluate_batch(ev, records, concurrency=2)
    assert len(scores) == 2
    assert scores[0].score == 1.0
    assert scores[1].score == 0.0


def test_evaluate_batch_sync() -> None:
    ev = ExactMatchEvaluator()
    scores = evaluate_batch_sync(
        ev,
        [{"output": "yes", "expected": "yes"}],
    )
    assert scores[0].label == "match"
