from pathlib import Path

from qapitol.evals import Score
from qapitol.evals.io import load_jsonl, write_jsonl, write_results_jsonl


def test_load_jsonl_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "data.jsonl"
    path.write_text(
        '{"id": "a"}\n\n  \n{"id": "b"}\n',
        encoding="utf-8",
    )
    records = load_jsonl(path)
    assert records == [{"id": "a"}, {"id": "b"}]


def test_write_jsonl_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "out.jsonl"
    records = [{"id": "1", "output": "x"}, {"id": "2", "output": "y"}]
    write_jsonl(path, records)
    assert load_jsonl(path) == records


def test_write_jsonl_empty(tmp_path: Path) -> None:
    path = tmp_path / "empty.jsonl"
    write_jsonl(path, [])
    assert path.read_text(encoding="utf-8") == ""


def test_write_results_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "results.jsonl"
    record = {"id": "t1", "input": "q", "output": "a"}
    scores = [
        Score(
            score=1.0,
            name="exact_match",
            label="match",
            kind="code",
        )
    ]
    write_results_jsonl(path, [(record, scores)])
    loaded = load_jsonl(path)
    assert loaded[0]["id"] == "t1"
    assert loaded[0]["scores"][0]["name"] == "exact_match"
    assert loaded[0]["scores"][0]["score"] == 1.0
