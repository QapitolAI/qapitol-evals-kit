from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from qapitol.evals.score import Score


def load_jsonl(path: Path | str) -> list[dict[str, Any]]:
    """Load JSONL file; skip blank lines."""
    text = Path(path).read_text(encoding="utf-8")
    records: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def write_jsonl(path: Path | str, records: Iterable[dict[str, Any]]) -> None:
    """Write one JSON object per line."""
    lines = [json.dumps(record, ensure_ascii=False) for record in records]
    Path(path).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_results_jsonl(
    path: Path | str,
    rows: Iterable[tuple[dict[str, Any], list[Score]]],
) -> None:
    """Write evaluation results: each record merged with serialized scores."""
    out: list[dict[str, Any]] = []
    for record, scores in rows:
        row = dict(record)
        row["scores"] = [s.model_dump() for s in scores]
        out.append(row)
    write_jsonl(path, out)
