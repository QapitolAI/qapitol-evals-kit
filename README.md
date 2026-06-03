# qapitol-evals-kit

Local **BYOK** LLM and RAG evaluation metrics from [Qapitol](https://github.com/QapitolAI). Your data never leaves your machine.

## Install

**PyPI** (after [publish setup](docs/RELEASING.md)):

```bash
pip install qapitol-evals-kit==0.1.0
pip install "qapitol-evals-kit[all]==0.1.0"   # OpenAI + Anthropic judges
```

**From source** (development):

```bash
pip install -e ".[dev,all]"
```

**From GitHub** (fallback):

```bash
pip install "qapitol-evals-kit @ git+https://github.com/QapitolAI/qapitol-evals-kit@v0.1.0"
pip install "qapitol-evals-kit @ git+https://github.com/QapitolAI/qapitol-evals-kit.git@main"
```

Repo: [github.com/QapitolAI/qapitol-evals-kit](https://github.com/QapitolAI/qapitol-evals-kit) · Releases: [v0.1.0](https://github.com/QapitolAI/qapitol-evals-kit/releases/tag/v0.1.0) · PyPI: [qapitol-evals-kit](https://pypi.org/project/qapitol-evals-kit/)

## Quick start (no API key)

```python
from qapitol.evals import ExactMatchEvaluator

score = ExactMatchEvaluator().evaluate({
    "output": "Paris",
    "expected": "Paris",
})
print(score.score, score.label)  # 1.0 match
```

## Quick start (LLM judge)

```bash
export OPENAI_API_KEY=sk-...
```

```python
from qapitol.evals import CoherenceEvaluator
from qapitol.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
score = CoherenceEvaluator(llm).evaluate({
    "input": "What is RAG?",
    "output": "RAG retrieves context then generates an answer.",
})
print(score.score, score.label, score.explanation)
```

## CLI

```bash
qapitol-evals doctor
qapitol-evals run --metric coherence --input "What is AI?" --output "AI is ..."
```

## Metrics (v0.1.0)

| Type | Evaluators |
|------|------------|
| Code | `ExactMatchEvaluator`, `CustomAccuracyEvaluator` |
| LLM | Coherence, Relevance, Correctness, Hallucination, Toxicity |
| RAG | Faithfulness, Answer Relevancy |

## Test

```bash
ruff check src tests
pytest tests/ -v
```

For agents working on this repo, see [`agent.md`](agent.md).

## License

MIT
