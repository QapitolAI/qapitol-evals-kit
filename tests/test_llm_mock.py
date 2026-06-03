import json

import pytest

from qapitol.evals.evaluators.llm_judge import (
    AnswerRelevancyEvaluator,
    CoherenceEvaluator,
    CorrectnessEvaluator,
    FaithfulnessEvaluator,
    HallucinationEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator,
)
from qapitol.evals.llm.wrapper import LLM, parse_judge_json
from qapitol.evals.testing import MockCompletionClient


def test_parse_judge_json_raw() -> None:
    data = parse_judge_json('{"score": 0.85, "label": "coherent", "explanation": "ok"}')
    assert data["score"] == 0.85


def test_parse_judge_json_embedded() -> None:
    data = parse_judge_json('Here is the result: {"score": 1.0, "label": "x", "explanation": "y"}')
    assert data["score"] == 1.0


@pytest.mark.parametrize(
    "evaluator_cls,record,response",
    [
        (
            CoherenceEvaluator,
            {"input": "What is AI?", "output": "AI is artificial intelligence."},
            json.dumps({"score": 0.9, "label": "coherent", "explanation": "clear"}),
        ),
        (
            RelevanceEvaluator,
            {"input": "Capital of France?", "output": "Paris."},
            json.dumps({"score": 0.95, "label": "relevant", "explanation": "on topic"}),
        ),
        (
            CorrectnessEvaluator,
            {
                "input": "2+2?",
                "output": "4",
                "expected": "4",
            },
            json.dumps({"score": 1.0, "label": "correct", "explanation": "right"}),
        ),
        (
            HallucinationEvaluator,
            {
                "input": "Q",
                "output": "From the doc: X.",
                "context": "The doc says X.",
            },
            json.dumps({"score": 0.9, "label": "grounded", "explanation": "supported"}),
        ),
        (
            ToxicityEvaluator,
            {"output": "Hello there."},
            json.dumps({"score": 0.05, "label": "safe", "explanation": "benign"}),
        ),
        (
            FaithfulnessEvaluator,
            {"output": "X only.", "context": "Only X in source."},
            json.dumps({"score": 0.88, "label": "faithful", "explanation": "ok"}),
        ),
        (
            AnswerRelevancyEvaluator,
            {
                "input": "What is RAG?",
                "output": "Retrieval augmented generation.",
                "context": "RAG combines retrieval and generation.",
            },
            json.dumps({"score": 0.92, "label": "relevant", "explanation": "answers Q"}),
        ),
    ],
)
def test_llm_evaluators_mocked(evaluator_cls, record, response, mock_llm: LLM) -> None:
    mock_llm._client = MockCompletionClient({"evaluator": response})  # type: ignore[attr-defined]
    ev = evaluator_cls(mock_llm)
    score = ev.evaluate(record)
    assert 0.0 <= score.score <= 1.0
    assert score.kind == "llm"
    assert score.name == ev.name


def test_toxicity_inverts_high_toxicity_score() -> None:
    client = MockCompletionClient()
    llm = LLM(provider="openai", model="test", client=client)
    ev = ToxicityEvaluator(llm)

    class FixedClient:
        def complete(self, prompt: str) -> str:
            return json.dumps({"score": 0.8, "label": "toxic", "explanation": "rude"})

    llm._client = FixedClient()  # type: ignore[assignment]
    score = ev.evaluate({"output": "bad"})
    assert score.score == pytest.approx(0.2)
