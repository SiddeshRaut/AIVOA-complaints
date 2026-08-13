"""Bonus feature: Duplicate Complaint Detection, run as a graph node against the
freshly extracted fields (a second check against the live/edited form happens
separately via POST /api/complaints/check-duplicates right before Save).
"""

from collections.abc import Callable

from sqlalchemy.orm import Session

from app.agents.state import ExtractionState
from app.services.duplicate_service import find_duplicates


def make_duplicate_check_node(db: Session) -> Callable[[ExtractionState], dict]:
    def duplicate_check(state: ExtractionState) -> dict:
        fields = state.get("extracted_fields", {})
        product_name = (fields.get("product_name") or {}).get("value") or ""
        batch_number = (fields.get("batch_number") or {}).get("value") or ""
        complaint_type = (fields.get("complaint_type") or {}).get("value") or ""
        description = (fields.get("description") or {}).get("value") or ""

        if not (product_name or batch_number or description):
            return {"duplicate_candidates": []}

        candidates = find_duplicates(
            db,
            product_name=product_name,
            batch_number=batch_number,
            complaint_type=complaint_type,
            description=description,
        )
        return {"duplicate_candidates": candidates}

    return duplicate_check
