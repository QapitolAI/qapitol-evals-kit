"""Batch JSONL evaluation with mocked LLM judge (no API key)."""

import json
from pathlib import Path

from qapitol.evals import (
    CoherenceEvaluator,
    ExactMatchEvaluator,
    load_jsonl,
    run_metrics,
    summarize,
    write_results_jsonl,
)
from qapitol.evals.llm import LLM
from qapitol.evals.testing import MockCompletionClient

DATA = Path(__file__).resolve().parent / "data" / "sample_traces.jsonl"
OUT = Path(__file__).resolve().parent / "data" / "results.jsonl"


def main() -> None:
    records = load_jsonl(DATA)
    client = MockCompletionClient(
        {
            "coherence": json.dumps(
                {
                    "score": 0.85,
                    "label": "coherent",
                    "explanation": "Clear and logical.",
                }
            ),
        }
    )
    llm = LLM(provider="openai", model="test", client=client)
    evaluators = [ExactMatchEvaluator(), CoherenceEvaluator(llm)]

    results = run_metrics(records, evaluators, concurrency=2)

    by_metric: dict[str, list] = {}
    for row in results:
        for s in row["scores"]:
            by_metric.setdefault(s.name, []).append(s)
    print("Summary:", summarize(by_metric))

    write_results_jsonl(OUT, [(row, row["scores"]) for row in results])
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
