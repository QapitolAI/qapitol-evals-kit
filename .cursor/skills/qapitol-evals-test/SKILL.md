---
name: qapitol-evals-test
description: Run ruff and pytest (mocked LLM) for qapitol-evals-kit before claiming done or pushing. Use when implementing or verifying evaluators.
disable-model-invocation: true
---

# qapitol-evals-test

## When to use

Before every push, after metric or LLM changes, when the user asks to test the implementation.

## Steps

1. `cd` to repo root (folder with `pyproject.toml`).
2. `python -m venv .venv` if missing; activate; `pip install -e ".[dev,all]"`.
3. `ruff check src tests`
4. `pytest tests/ -v` — must pass without API keys.
5. Optional live: `QAPITOL_EVALS_LIVE=1 pytest tests/ -m live -v` (only if user has keys).
6. `qapitol-evals doctor` when CLI exists.
7. Report pass/fail. Do not push if ruff or pytest fails.
8. Update `.plan/IMPLEMENTATION_TRACKER.md` (last verified date, session log if meaningful).
