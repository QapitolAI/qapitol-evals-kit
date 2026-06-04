from __future__ import annotations

from typing import Any

_ROLE_LABELS = {"user": "User", "assistant": "Assistant", "system": "System"}


def format_transcript(
    messages: list[dict[str, Any]],
    *,
    max_chars: int | None = None,
) -> str:
    """Format messages as a plain-text transcript for judge input."""
    lines: list[str] = []
    for msg in messages:
        role = str(msg.get("role", "user"))
        label = _ROLE_LABELS.get(role, role.capitalize())
        lines.append(f"{label}: {msg.get('content', '')}")
    text = "\n".join(lines)
    if max_chars is not None and len(text) > max_chars:
        return "...\n" + text[-max_chars:]
    return text


def records_per_turn(session: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand a session into one record per assistant turn."""
    messages = session.get("messages", [])
    session_id = session.get("session_id")
    base_metadata = dict(session.get("metadata") or {})
    context = session.get("context")
    records: list[dict[str, Any]] = []
    turn = 0

    for i, msg in enumerate(messages):
        if msg.get("role") != "assistant":
            continue
        turn += 1
        user_input = ""
        for prior in reversed(messages[:i]):
            if prior.get("role") == "user":
                user_input = str(prior.get("content", ""))
                break
        record: dict[str, Any] = {
            "input": user_input,
            "output": str(msg.get("content", "")),
        }
        if session_id is not None:
            record["id"] = f"{session_id}-turn-{turn}"
        metadata = {**base_metadata, "session_id": session_id, "turn": turn}
        record["metadata"] = metadata
        if context is not None:
            record["context"] = context
        records.append(record)
    return records


def record_final_turn(session: dict[str, Any]) -> dict[str, Any]:
    """Build a single record from the last user/assistant pair."""
    messages = session.get("messages", [])
    last_user = ""
    last_assistant = ""
    for msg in messages:
        role = msg.get("role")
        if role == "user":
            last_user = str(msg.get("content", ""))
        elif role == "assistant":
            last_assistant = str(msg.get("content", ""))

    record: dict[str, Any] = {
        "input": last_user,
        "output": last_assistant,
    }
    session_id = session.get("session_id")
    if session_id is not None:
        record["id"] = session_id
    metadata = dict(session.get("metadata") or {})
    if session_id is not None:
        metadata["session_id"] = session_id
    if metadata:
        record["metadata"] = metadata
    context = session.get("context")
    if context is not None:
        record["context"] = context
    return record
