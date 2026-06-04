from qapitol.evals.conversation import (
    format_transcript,
    record_final_turn,
    records_per_turn,
)

SESSION = {
    "session_id": "s1",
    "messages": [
        {"role": "user", "content": "What is ML?"},
        {"role": "assistant", "content": "Machine learning learns from data."},
        {"role": "user", "content": "Give an example."},
        {"role": "assistant", "content": "Email spam filters use ML."},
    ],
    "context": "wiki excerpt",
    "metadata": {"product": "demo"},
}


def test_format_transcript() -> None:
    text = format_transcript(SESSION["messages"])
    assert "User: What is ML?" in text
    assert "Assistant: Machine learning learns from data." in text
    assert "User: Give an example." in text


def test_format_transcript_max_chars() -> None:
    text = format_transcript(SESSION["messages"], max_chars=30)
    assert text.startswith("...")
    assert len(text) <= 30 + 4  # "...\n" prefix


def test_records_per_turn() -> None:
    records = records_per_turn(SESSION)
    assert len(records) == 2
    assert records[0]["input"] == "What is ML?"
    assert records[0]["output"] == "Machine learning learns from data."
    assert records[0]["id"] == "s1-turn-1"
    assert records[0]["context"] == "wiki excerpt"
    assert records[0]["metadata"]["turn"] == 1
    assert records[1]["input"] == "Give an example."
    assert records[1]["output"] == "Email spam filters use ML."


def test_record_final_turn() -> None:
    record = record_final_turn(SESSION)
    assert record["input"] == "Give an example."
    assert record["output"] == "Email spam filters use ML."
    assert record["id"] == "s1"
    assert record["context"] == "wiki excerpt"
    assert record["metadata"]["product"] == "demo"
