from typing import TypedDict


class ExtractionState(TypedDict, total=False):
    document_id: int
    document_text: str
    extracted_fields: dict[str, dict]
    missing_required_fields: list[str]
    low_confidence_fields: list[str]
    risk_severity: str | None
    risk_priority: str | None
    risk_rationale: str | None
    duplicate_candidates: list[dict]
    warnings: list[str]


class ChatState(TypedDict, total=False):
    message: str
    document_text: str
    form_snapshot: dict
    history: list[dict]
    context: str
    answer: str
