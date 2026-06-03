"""Code-based metrics without API keys."""

from qapitol.evals import CustomAccuracyEvaluator, ExactMatchEvaluator


def main() -> None:
    exact = ExactMatchEvaluator()
    s1 = exact.evaluate({"output": "42", "expected": "42"})
    print(f"exact_match: {s1.score} ({s1.label})")

    acc = CustomAccuracyEvaluator(mode="contains")
    s2 = acc.evaluate({"output": "The capital is Paris.", "expected": "Paris"})
    print(f"custom_accuracy: {s2.score} ({s2.label})")


if __name__ == "__main__":
    main()
