"""Bonus feature: Complaint Completeness Checker.

Pure Python — no LLM call needed. Flags which required fields the extraction
missed and which extracted values it wasn't confident about, so QA staff know
exactly what to verify or follow up on with the customer before triage.
"""

from app.agents.state import ExtractionState

REQUIRED_FIELDS = [
    "customer_name",
    "product_name",
    "batch_number",
    "complaint_type",
    "complaint_date",
    "description",
]
LOW_CONFIDENCE_THRESHOLD = 0.6


def completeness_check(state: ExtractionState) -> dict:
    fields = state.get("extracted_fields", {})

    missing_required = [
        name for name in REQUIRED_FIELDS if not (fields.get(name) or {}).get("value")
    ]
    low_confidence = [
        name
        for name, field in fields.items()
        if field.get("value") and field.get("confidence", 0.0) < LOW_CONFIDENCE_THRESHOLD
    ]

    return {
        "missing_required_fields": missing_required,
        "low_confidence_fields": low_confidence,
    }
