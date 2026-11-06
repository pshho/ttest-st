"""Normalize labels for the Paperclip smoke test."""


def normalize_label(text: str) -> str:
    """Return a lowercase label with trimmed, collapsed whitespace."""
    return " ".join(text.lower().split())
