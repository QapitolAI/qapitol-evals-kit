import pytest

from qapitol.evals.evaluators.code import CustomAccuracyEvaluator, ExactMatchEvaluator


def test_exact_match_success() -> None:
    ev = ExactMatchEvaluator()
    score = ev.evaluate({"output": "Hello", "expected": "Hello"})
    assert score.score == 1.0
    assert score.label == "match"


def test_exact_match_case_insensitive() -> None:
    ev = ExactMatchEvaluator(case_sensitive=False)
    score = ev.evaluate({"output": "hello", "expected": "HELLO"})
    assert score.score == 1.0


def test_exact_match_missing_expected() -> None:
    ev = ExactMatchEvaluator()
    with pytest.raises(ValueError, match="expected"):
        ev.evaluate({"output": "x"})


def test_custom_accuracy_contains() -> None:
    ev = CustomAccuracyEvaluator(mode="contains")
    score = ev.evaluate({"output": "The answer is Paris.", "expected": "Paris"})
    assert score.score == 1.0


def test_custom_accuracy_regex() -> None:
    ev = CustomAccuracyEvaluator(mode="regex")
    score = ev.evaluate({"output": "id=12345", "expected": r"\d+"})
    assert score.score == 1.0
