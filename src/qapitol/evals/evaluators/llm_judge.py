from __future__ import annotations

from typing import Any, Callable

from qapitol.evals.base import BaseEvaluator
from qapitol.evals.llm.wrapper import LLM, parse_judge_json
from qapitol.evals.score import Score


class LLMJudgeEvaluator(BaseEvaluator):
    """Base for LLM-as-judge metrics."""

    def __init__(
        self,
        llm: LLM,
        *,
        name: str,
        template: str,
        required_fields: list[str],
        label_positive: str,
        invert_score: bool = False,
    ) -> None:
        self.llm = llm
        self.name = name
        self.template = template
        self.required_fields = required_fields
        self.label_positive = label_positive
        self.invert_score = invert_score

    def evaluate(self, record: dict[str, Any]) -> Score:
        self._require_fields(record, self.required_fields)
        prompt = self.template.format(
            input=record.get("input", ""),
            output=record.get("output", ""),
            context=record.get("context", ""),
            expected=record.get("expected", ""),
        )
        raw = self.llm.complete(prompt)
        data = parse_judge_json(raw)
        score_val = float(data.get("score", 0.0))
        score_val = max(0.0, min(1.0, score_val))
        if self.invert_score:
            score_val = 1.0 - score_val
        label = str(data.get("label", "unknown"))
        explanation = str(data.get("explanation", ""))
        return Score(
            score=score_val,
            name=self.name,
            label=label,
            explanation=explanation,
            kind="llm",
            direction="maximize",
            metadata={"provider": self.llm.provider, "model": self.llm.model},
        )


def _make_llm_evaluator(
    llm: LLM,
    name: str,
    template: str,
    required_fields: list[str],
    label_positive: str,
    *,
    invert_score: bool = False,
) -> LLMJudgeEvaluator:
    return LLMJudgeEvaluator(
        llm,
        name=name,
        template=template,
        required_fields=required_fields,
        label_positive=label_positive,
        invert_score=invert_score,
    )


def build_llm_evaluator(
    llm: LLM,
    metric: str,
) -> BaseEvaluator:
    builders: dict[str, Callable[[LLM], BaseEvaluator]] = {
        "coherence": lambda m: CoherenceEvaluator(m),
        "relevance": lambda m: RelevanceEvaluator(m),
        "correctness": lambda m: CorrectnessEvaluator(m),
        "hallucination": lambda m: HallucinationEvaluator(m),
        "toxicity": lambda m: ToxicityEvaluator(m),
        "faithfulness": lambda m: FaithfulnessEvaluator(m),
        "answer_relevancy": lambda m: AnswerRelevancyEvaluator(m),
    }
    if metric not in builders:
        raise ValueError(f"Unknown metric: {metric}")
    return builders[metric](llm)


class CoherenceEvaluator(LLMJudgeEvaluator):
    def __init__(self, llm: LLM) -> None:
        from qapitol.evals.prompts import templates

        super().__init__(
            llm,
            name="coherence",
            template=templates.COHERENCE,
            required_fields=["input", "output"],
            label_positive="coherent",
        )


class RelevanceEvaluator(LLMJudgeEvaluator):
    def __init__(self, llm: LLM) -> None:
        from qapitol.evals.prompts import templates

        super().__init__(
            llm,
            name="relevance",
            template=templates.RELEVANCE,
            required_fields=["input", "output"],
            label_positive="relevant",
        )


class CorrectnessEvaluator(LLMJudgeEvaluator):
    def __init__(self, llm: LLM) -> None:
        from qapitol.evals.prompts import templates

        super().__init__(
            llm,
            name="correctness",
            template=templates.CORRECTNESS,
            required_fields=["input", "output", "expected"],
            label_positive="correct",
        )


class HallucinationEvaluator(LLMJudgeEvaluator):
    def __init__(self, llm: LLM) -> None:
        from qapitol.evals.prompts import templates

        super().__init__(
            llm,
            name="hallucination",
            template=templates.HALLUCINATION,
            required_fields=["input", "output", "context"],
            label_positive="grounded",
        )


class ToxicityEvaluator(LLMJudgeEvaluator):
    def __init__(self, llm: LLM) -> None:
        from qapitol.evals.prompts import templates

        super().__init__(
            llm,
            name="toxicity",
            template=templates.TOXICITY,
            required_fields=["output"],
            label_positive="safe",
            invert_score=True,
        )


class FaithfulnessEvaluator(LLMJudgeEvaluator):
    def __init__(self, llm: LLM) -> None:
        from qapitol.evals.prompts import templates

        super().__init__(
            llm,
            name="faithfulness",
            template=templates.FAITHFULNESS,
            required_fields=["output", "context"],
            label_positive="faithful",
        )


class AnswerRelevancyEvaluator(LLMJudgeEvaluator):
    def __init__(self, llm: LLM) -> None:
        from qapitol.evals.prompts import templates

        super().__init__(
            llm,
            name="answer_relevancy",
            template=templates.ANSWER_RELEVANCY,
            required_fields=["input", "output", "context"],
            label_positive="relevant",
        )
