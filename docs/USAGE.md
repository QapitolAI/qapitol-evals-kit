# qapitol-evals-kit — Usage guide

Run standard LLM and RAG evaluation metrics **locally** with **your API keys**. No Qapitol account required; your data stays in your environment.

**Version:** 0.1.x · **Repo:** [github.com/QapitolAI/qapitol-evals-kit](https://github.com/QapitolAI/qapitol-evals-kit)

> **After `pip install`:** this guide lives on **GitHub** (not inside the installed wheel). Bookmark this page or use the **Documentation** link on [PyPI](https://pypi.org/project/qapitol-evals-kit/).

---

## 1. Who this is for

- ML / LLM engineers adding evals to notebooks or CI
- QA / eval leads who want coherence, relevance, RAG faithfulness, etc. without writing judges from scratch
- Teams with data-sovereignty rules (BYOK only; no trace upload to Qapitol)

### What you can do (v0.1)

| Capability | Supported |
|------------|-----------|
| Score a single model response | Yes — Python API or CLI |
| Score many rows in Python | Yes — `evaluate_batch_sync` |
| Code metrics without API keys | Yes — exact match, custom accuracy |
| LLM-as-judge metrics (OpenAI / Anthropic) | Yes — BYOK |
| RAG metrics (faithfulness, answer relevancy) | Yes — with `context` |
| Read traces from JSONL in one command | No — use Python + stdlib `json` (v0.2 will add helpers) |
| Native multi-turn / `messages[]` API | No — use patterns in [§5.5](#55-multi-turn-conversations-v01) |
| Upload traces to Qapitol | No — use [Qapitol QAVE / Qurator](https://github.com/QapitolAI) for hosted evals |

---

## 2. Install

```bash
pip install qapitol-evals-kit==0.1.1
pip install "qapitol-evals-kit[all]==0.1.1"   # OpenAI + Anthropic client libraries
```

Verify:

```bash
qapitol-evals doctor
```

Expected (API keys optional for `doctor`):

```text
qapitol-evals doctor
  Python: 3.10.x
  OPENAI_API_KEY: not set
  ANTHROPIC_API_KEY: not set
  Code metric smoke (exact_match): match score=1.0
```

### Environment variables

| Variable | Used for |
|----------|----------|
| `OPENAI_API_KEY` | `LLM(provider="openai", ...)` |
| `ANTHROPIC_API_KEY` | `LLM(provider="anthropic", ...)` |

Set in your shell or CI secret store. **Never commit keys** to git.

---

## 3. Core concepts

### Record

Every evaluation takes one **record**: a plain Python `dict`. Evaluators read these keys:

| Field | Meaning |
|-------|---------|
| `input` | User question or prompt |
| `output` | Model or agent response to judge |
| `context` | Retrieved text, tool output, or grounding source (RAG) |
| `expected` | Reference / gold answer |

Extra keys (`id`, `metadata`, etc.) are ignored by evaluators but useful for your reporting.

### Evaluator → Score

```python
from qapitol.evals import CoherenceEvaluator
from qapitol.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
score = CoherenceEvaluator(llm).evaluate({
    "input": "What is RAG?",
    "output": "RAG retrieves context then generates an answer.",
})

print(score.score)        # 0.0–1.0
print(score.label)        # e.g. "coherent"
print(score.explanation)  # judge reasoning
print(score.passed_threshold(0.8))  # True / False
```

| `Score` field | Meaning |
|---------------|---------|
| `score` | Numeric 0.0–1.0 |
| `name` | Metric name |
| `label` | Categorical label from judge or rules |
| `explanation` | Text reasoning (LLM metrics) |
| `kind` | `"code"` or `"llm"` |
| `direction` | `"maximize"` (higher is better) or `"minimize"` |
| `metadata` | e.g. provider, model id |

### LLM wrapper

```python
from qapitol.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")       # default
llm = LLM(provider="anthropic", model="claude-3-5-haiku-latest")
```

Each LLM metric call sends **one judge prompt** to your provider. Cost ≈ `number_of_rows × number_of_LLM_metrics`.

---

## 4. Evaluator reference

### Code metrics (no API key)

| Evaluator | Required fields | Example record | Notes |
|-----------|-----------------|----------------|-------|
| `ExactMatchEvaluator` | `output`, `expected` | `{"output": "Paris", "expected": "Paris"}` | Binary 0/1; optional `case_sensitive`, `strip` |
| `CustomAccuracyEvaluator` | `output`, `expected` | `{"output": "The capital is Paris.", "expected": "Paris"}` | `mode`: `"contains"`, `"regex"`, or `"equal"` |

```python
from qapitol.evals import ExactMatchEvaluator, CustomAccuracyEvaluator

ExactMatchEvaluator().evaluate({"output": "42", "expected": "42"})
CustomAccuracyEvaluator(mode="contains").evaluate({
    "output": "Answer: 42 units.",
    "expected": "42",
})
```

### LLM metrics (BYOK)

| Evaluator | Required fields | CLI `--metric` | Notes |
|-----------|-----------------|----------------|-------|
| `CoherenceEvaluator` | `input`, `output` | `coherence` | Response logical vs question |
| `RelevanceEvaluator` | `input`, `output` | `relevance` | On-topic vs question |
| `CorrectnessEvaluator` | `input`, `output`, `expected` | `correctness` | vs reference answer |
| `HallucinationEvaluator` | `input`, `output`, `context` | `hallucination` | Grounded in context |
| `ToxicityEvaluator` | `output` | `toxicity` | Safety; higher score = safer |
| `FaithfulnessEvaluator` | `output`, `context` | `faithfulness` | Claims supported by context |
| `AnswerRelevancyEvaluator` | `input`, `output`, `context` | `answer_relevancy` | Answer addresses question given context |

Example — RAG faithfulness:

```python
from qapitol.evals import FaithfulnessEvaluator
from qapitol.evals.llm import LLM

llm = LLM(provider="openai", model="gpt-4o-mini")
score = FaithfulnessEvaluator(llm).evaluate({
    "output": "Returns are accepted within 30 days.",
    "context": "Policy: 30-day return window for all items.",
})
```

Missing required fields raise `ValueError` with the metric name and field list.

---

## 5. Workflows

### 5.1 Single evaluation (code)

```python
from qapitol.evals import ExactMatchEvaluator

score = ExactMatchEvaluator().evaluate({"output": "yes", "expected": "yes"})
assert score.passed_threshold(1.0)
```

### 5.2 Single evaluation (LLM)

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."  # or export in shell

from qapitol.evals import RelevanceEvaluator
from qapitol.evals.llm import LLM

score = RelevanceEvaluator(LLM()).evaluate({
    "input": "Capital of France?",
    "output": "Paris.",
})
```

### 5.3 Batch evaluation

```python
from qapitol.evals import ExactMatchEvaluator
from qapitol.evals.batch import evaluate_batch_sync

records = [
    {"output": "a", "expected": "a"},
    {"output": "b", "expected": "c"},
]
scores = evaluate_batch_sync(ExactMatchEvaluator(), records, concurrency=4)
for rec, sc in zip(records, scores):
    print(rec["output"], sc.score, sc.label)
```

For LLM metrics, each row triggers a judge API call. Tune `concurrency` to respect provider rate limits.

### 5.4 Multiple metrics on the same data

```python
from qapitol.evals import CoherenceEvaluator, ToxicityEvaluator
from qapitol.evals.llm import LLM

llm = LLM()
records = [{"input": "Hi", "output": "Hello! How can I help?"}]

for ev in (CoherenceEvaluator(llm), ToxicityEvaluator(llm)):
    for rec in records:
        s = ev.evaluate(rec)
        print(s.name, s.score, s.label)
```

**Cost:** `len(records) × number_of_LLM_evaluators` API calls.

### 5.5 Multi-turn conversations (v0.1)

There is no `messages[]` field on evaluators. Use one of these patterns:

**Pattern A — One row per turn**

Split a session into multiple records; each row judges one assistant reply.

```python
records = [
    {"input": "What is ML?", "output": "Machine learning learns from data."},
    {"input": "Give an example.", "output": "Email spam filters use ML."},
]
```

**Pattern B — Final turn only**

When you only care about the last answer:

```python
record = {
    "input": last_user_message,
    "output": last_assistant_message,
    "context": retrieved_chunks,  # if RAG
}
```

**Pattern C — Full transcript in `input`**

Paste prior turns into `input` as text; put the final reply in `output`.

```python
record = {
    "input": "User: What is RAG?\nAssistant: Retrieval augmented generation.\nUser: Why use it?",
    "output": "It reduces hallucinations by grounding answers in retrieved docs.",
}
```

Long transcripts increase judge tokens and cost.

### 5.6 Traces → records (JSONL)

Export traces from your observability tool, map columns to record fields, save as **JSONL** (one JSON object per line):

```json
{"id": "run-001", "input": "Refund policy?", "output": "30-day returns.", "context": "Policy doc excerpt..."}
```

Load and evaluate in Python (stdlib only in v0.1):

```python
import json
from pathlib import Path

from qapitol.evals import CoherenceEvaluator
from qapitol.evals.batch import evaluate_batch_sync
from qapitol.evals.llm import LLM

def load_jsonl(path: Path) -> list[dict]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records

records = load_jsonl(Path("traces.jsonl"))
llm = LLM()
scores = evaluate_batch_sync(CoherenceEvaluator(llm), records)

for rec, sc in zip(records, scores):
    print(rec.get("id", "?"), sc.score, sc.label)
```

| Your trace field | Map to |
|------------------|--------|
| User message / prompt | `input` |
| Assistant / model reply | `output` |
| Retrieved chunks (join with `\n\n`) | `context` |
| Gold label / expected answer | `expected` |

---

## 6. CLI

```bash
qapitol-evals doctor

qapitol-evals run --metric coherence \
  --input "What is AI?" \
  --output "AI is the simulation of human intelligence."

qapitol-evals run --metric faithfulness \
  --output "30-day returns." \
  --context "All items: 30-day return policy."

qapitol-evals run --metric correctness \
  --input "2+2?" --output "4" --expected "4" \
  --provider openai --model gpt-4o-mini
```

| Flag | Default | Purpose |
|------|---------|---------|
| `--metric` | (required) | See CLI names in §4 |
| `--input` | `""` | User question |
| `--output` | (required) | Model response |
| `--context` | `""` | RAG / grounding text |
| `--expected` | `""` | Reference answer |
| `--provider` | `openai` | `openai` or `anthropic` |
| `--model` | `gpt-4o-mini` | Provider model id |

**Limits (v0.1):**

- One row per command (no `--file` batch yet)
- Code metrics (`exact_match`, `custom_accuracy`) — use Python API or `examples/01_basic_code.py`

---

## 7. Examples (in the GitHub repo)

Clone or browse [examples/](https://github.com/QapitolAI/qapitol-evals-kit/tree/main/examples):

| File | What it shows |
|------|----------------|
| `01_basic_code.py` | `ExactMatchEvaluator`, `CustomAccuracyEvaluator` — no API key |
| `02_rag_mock.py` | `FaithfulnessEvaluator` with `MockCompletionClient` |
| `03_agent_smoke.py` | Coherence + relevance on agent output (mocked judge) |

Run from repo root after `pip install -e ".[dev,all]"`:

```bash
python examples/01_basic_code.py
python examples/02_rag_mock.py
python examples/03_agent_smoke.py
```

---

## 8. Testing without API keys

### Mock LLM in your code

```python
import json
from qapitol.evals import CoherenceEvaluator
from qapitol.evals.llm import LLM
from qapitol.evals.testing import MockCompletionClient

client = MockCompletionClient({
    "coherent": json.dumps({
        "score": 0.9,
        "label": "coherent",
        "explanation": "clear answer",
    }),
})
llm = LLM(provider="openai", model="test", client=client)
score = CoherenceEvaluator(llm).evaluate({
    "input": "Q",
    "output": "A",
})
```

`MockCompletionClient` returns JSON when a substring of the prompt matches a dict key; otherwise a default pass response.

### Project tests

From a source checkout:

```bash
pip install -e ".[dev,all]"
pytest tests/ -v
```

All default tests use mocks — no `OPENAI_API_KEY` required.

---

## 9. CI and thresholds

Gate a build on a minimum score:

```python
from qapitol.evals import CoherenceEvaluator
from qapitol.evals.llm import LLM

THRESHOLD = 0.8
score = CoherenceEvaluator(LLM()).evaluate({"input": "...", "output": "..."})

if not score.passed_threshold(THRESHOLD):
    raise SystemExit(f"FAIL {score.name}: {score.score} < {THRESHOLD}")
```

For CI without live API costs, use `MockCompletionClient` or run only code metrics in the pipeline. Live LLM tests should stay optional (separate job + secrets).

---

## 10. FAQ

**Where is this guide after `pip install`?**  
On GitHub: [docs/USAGE.md](https://github.com/QapitolAI/qapitol-evals-kit/blob/main/docs/USAGE.md). The installed package contains Python code and the `qapitol-evals` CLI only. Use the README or PyPI **Documentation** link.

**Do I need a Qapitol account?**  
No.

**What does it cost?**  
The kit is free (MIT). You pay your LLM provider for judge calls.

**Is my data sent to Qapitol?**  
No. Inference goes from your machine to your chosen provider (OpenAI, Anthropic, etc.).

**How is this different from Qapitol QAVE / Qurator?**  
The kit is local-only BYOK metrics. Hosted taxonomy, batch scoring at scale, and governance live in QAVE (UC1).

**Can I re-publish the same version to PyPI?**  
No. PyPI versions are immutable; ship fixes as `0.1.2`, etc.

**Which Python versions are supported?**  
Python 3.10+.

---

## Maintainer docs

- PyPI release process: [RELEASING.md](RELEASING.md)
- Contributing / agents: [agent.md](../agent.md) (repo root)
