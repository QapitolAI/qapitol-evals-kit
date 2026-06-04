"""Multi-turn conversation helpers (patterns A, B, C)."""

from qapitol.evals import ExactMatchEvaluator
from qapitol.evals.conversation import (
    format_transcript,
    record_final_turn,
    records_per_turn,
)

SESSION = {
    "session_id": "demo-1",
    "messages": [
        {"role": "user", "content": "What is ML?"},
        {"role": "assistant", "content": "Machine learning learns from data."},
        {"role": "user", "content": "Give an example."},
        {"role": "assistant", "content": "Email spam filters use ML."},
    ],
    "metadata": {"source": "example"},
}


def main() -> None:
    # Pattern A — one row per assistant turn
    per_turn = records_per_turn(SESSION)
    print(f"Pattern A: {len(per_turn)} records")
    for rec in per_turn:
        print(f"  turn {rec['metadata']['turn']}: {rec['input']!r} -> {rec['output']!r}")

    # Pattern B — final turn only
    final = record_final_turn(SESSION)
    print(f"Pattern B: input={final['input']!r} output={final['output']!r}")

    # Pattern C — full transcript in input
    transcript = format_transcript(SESSION["messages"][:-1])
    pattern_c = {**final, "input": transcript}
    print(f"Pattern C: input length={len(pattern_c['input'])} chars")

    # Score pattern A rows with a code metric (no API key)
    ev = ExactMatchEvaluator()
    for rec in per_turn:
        if "expected" in rec:
            score = ev.evaluate(rec)
            print(f"  score {rec.get('id')}: {score.score}")


if __name__ == "__main__":
    main()
