from __future__ import annotations

import argparse
import os
import sys

from qapitol.evals.evaluators.code import ExactMatchEvaluator
from qapitol.evals.evaluators.llm_judge import build_llm_evaluator
from qapitol.evals.llm.wrapper import LLM


def doctor() -> int:
    print("qapitol-evals doctor")
    print(f"  Python: {sys.version.split()[0]}")
    openai_key = bool(os.environ.get("OPENAI_API_KEY"))
    anthropic_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    print(f"  OPENAI_API_KEY: {'set' if openai_key else 'not set'}")
    print(f"  ANTHROPIC_API_KEY: {'set' if anthropic_key else 'not set'}")
    ev = ExactMatchEvaluator()
    score = ev.evaluate({"output": "hello", "expected": "hello"})
    print(f"  Code metric smoke (exact_match): {score.label} score={score.score}")
    return 0


def run_metric(args: argparse.Namespace) -> int:
    if args.metric in ("exact_match", "custom_accuracy"):
        print("Code metrics: use Python API or examples/01_basic_code.py")
        return 1
    llm = LLM(provider=args.provider, model=args.model)
    evaluator = build_llm_evaluator(llm, args.metric)
    record = {"input": args.input, "output": args.output}
    if args.context:
        record["context"] = args.context
    if args.expected:
        record["expected"] = args.expected
    score = evaluator.evaluate(record)
    print(f"{score.name}: {score.score:.2f} ({score.label})")
    if score.explanation:
        print(score.explanation)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="qapitol-evals")
    sub = parser.add_subparsers(dest="command", required=True)
    doc = sub.add_parser("doctor")
    doc.set_defaults(func=lambda _a: doctor())
    run_p = sub.add_parser("run")
    run_p.add_argument("--metric", required=True)
    run_p.add_argument("--input", default="")
    run_p.add_argument("--output", required=True)
    run_p.add_argument("--context", default="")
    run_p.add_argument("--expected", default="")
    run_p.add_argument("--provider", default="openai")
    run_p.add_argument("--model", default="gpt-4o-mini")
    run_p.set_defaults(func=run_metric)
    args = parser.parse_args()
    raise SystemExit(args.func(args))
