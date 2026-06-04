from qapitol.evals import ExactMatchEvaluator
from qapitol.evals.runner import run_metrics, summarize


def test_run_metrics_multiple_evaluators() -> None:
    records = [
        {"output": "a", "expected": "a"},
        {"output": "b", "expected": "c"},
    ]
    results = run_metrics(records, [ExactMatchEvaluator()])
    assert len(results) == 2
    assert results[0]["scores"][0].score == 1.0
    assert results[1]["scores"][0].score == 0.0
    assert results[0]["output"] == "a"


def test_run_metrics_empty_evaluators() -> None:
    records = [{"output": "x"}]
    results = run_metrics(records, [])
    assert results == [{"output": "x"}]


def test_summarize() -> None:
    from qapitol.evals import Score

    scores_by_metric = {
        "exact_match": [
            Score(score=1.0, name="exact_match", label="match", kind="code"),
            Score(score=0.0, name="exact_match", label="no_match", kind="code"),
        ],
    }
    assert summarize(scores_by_metric) == {"exact_match": 0.5}
