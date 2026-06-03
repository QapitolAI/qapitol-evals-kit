"""Agent output evaluation smoke test (mocked LLM judge)."""

import json

from qapitol.evals import CoherenceEvaluator, RelevanceEvaluator
from qapitol.evals.llm import LLM
from qapitol.evals.testing import MockCompletionClient


def fake_agent(query: str) -> str:
    return "Machine learning is a subset of AI focused on learning from data."


def main() -> None:
    query = "What is machine learning?"
    response = fake_agent(query)
    client = MockCompletionClient(
        {
            "coherent": json.dumps(
                {"score": 0.9, "label": "coherent", "explanation": "clear"}
            ),
            "relevant": json.dumps(
                {"score": 0.85, "label": "relevant", "explanation": "on topic"}
            ),
        }
    )
    llm = LLM(provider="openai", model="test", client=client)
    record = {"input": query, "output": response}
    for ev in (CoherenceEvaluator(llm), RelevanceEvaluator(llm)):
        s = ev.evaluate(record)
        print(f"{s.name}: {s.score:.2f} ({s.label})")


if __name__ == "__main__":
    main()
