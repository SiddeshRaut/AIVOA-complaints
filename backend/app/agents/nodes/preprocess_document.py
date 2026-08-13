import re

from app.agents.state import ExtractionState

MAX_CHARS = 8000  # keeps prompt comfortably within the small extraction model's context budget


def preprocess_document(state: ExtractionState) -> dict:
    text = state.get("document_text", "") or ""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n[...truncated...]"
    return {"document_text": text}
