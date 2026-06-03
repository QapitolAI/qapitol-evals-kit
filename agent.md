# Qapitol Evals Kit — Agent context

## Product

**UC4 Evals Kit** (`qapitol-evals-kit`): run standard LLM/RAG evaluation metrics **locally** with **BYOK** API keys. Free forever. No data sent to Qapitol servers.

- **GitHub:** `QapitolAI/qapitol-evals-kit`
- **Import:** `qapitol.evals`
- **PyPI (when live):** `qapitol-evals-kit`

## Architecture

Greenfield library: `Evaluator.evaluate(eval_dict)` → optional `LLM` call → `Score`.

- **Code metrics:** no API keys
- **LLM / RAG metrics:** judge prompts + BYOK (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)

**Not in v1:** RAGAS, Promptfoo, DeepEval, phoenix-evals, hosted QAVE, 17 framework plugins, OCR/Textract.

## Git commits (Qapitol identity only)

This repo uses **local** git config (not personal global email):

| Setting | Value |
|---------|--------|
| `user.name` | `Qapitol` |
| `user.email` | `satyam.dixit@qapitol.com` |

Before commit/push: `./scripts/verify-git-identity.sh`

**Never** add `Co-authored-by: Cursor` or `cursoragent@cursor.com` to commits. Agents must not attribute work to Cursor on GitHub.

One-time on your machine (strips IDE-injected co-author lines):

```bash
./scripts/install-git-hooks.sh
```

In **Cursor Settings**, disable agent commit co-author / attribution if that option exists.

Before push, `./scripts/verify-git-identity.sh` must pass (fails if Cursor co-author is still on `HEAD`).

## Coding standards

- Python 3.10+, type hints, pydantic v2
- Minimal dependencies; no secrets in repo
- Run **qapitol-evals-test** skill before every push
- Run **qapitol-evals-github** skill when pushing to `QapitolAI`

## Third-party libraries

Use **Context7 MCP** for current docs before integrating `openai`, `anthropic`, `pydantic`, or build tooling. Do not guess provider APIs.

## Security

- Keys via environment variables only
- CI uses mocked LLM responses by default
- Never commit `.env` or API keys

## Cross-sell

Users needing error taxonomy or hosted scoring → Qapitol QAVE / Qurator (UC1).

## Implementation progress (agents)

Local tracker (gitignored, not on GitHub): **`.plan/IMPLEMENTATION_TRACKER.md`**

- Open it at the **start** of a new session for what is implemented vs pending.
- **Update** it at the **end** of each session (session log + phase checklist + last pytest run).
