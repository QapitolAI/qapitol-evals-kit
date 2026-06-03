"""RAG metrics with a mocked judge (no API key)."""

import json

from qapitol.evals import FaithfulnessEvaluator
from qapitol.evals.llm import LLM
from qapitol.evals.testing import MockCompletionClient


def main() -> None:
    client = MockCompletionClient(
        {
            "faithfulness": json.dumps(
                {
                    "score": 0.95,
                    "label": "faithful",
                    "explanation": "Claims match context.",
                }
            )
        }
    )
    llm = LLM(provider="openai", model="test", client=client)
    ev = FaithfulnessEvaluator(llm)
    score = ev.evaluate(
        {
            "output": "RAG combines retrieval with generation.",
            "context": "RAG is retrieval augmented generation.",
        }
    )
    print(f"faithfulness: {score.score} ({score.label})")


if __name__ == "__main__":
    main()
