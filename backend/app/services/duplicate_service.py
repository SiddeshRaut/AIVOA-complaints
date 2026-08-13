"""Bonus feature: Duplicate Complaint Detection.

Two-stage approach chosen because MySQL FULLTEXT relevance scoring is unreliable
on a small corpus (natural-language mode can silently drop common terms with only
a handful of rows). Stage 1 is a cheap SQL prefilter to bound the candidate set;
stage 2 does the real similarity scoring in Python with rapidfuzz, which doesn't
have that small-corpus weakness.
"""

from sqlalchemy import or_, text
from sqlalchemy.orm import Session
from rapidfuzz import fuzz

from app.models.complaint import Complaint

SCORE_THRESHOLD = 40.0
MAX_CANDIDATES = 5
PREFILTER_LIMIT = 25


def _prefilter(
    db: Session,
    product_name: str,
    batch_number: str,
    complaint_type: str,
    description: str,
    exclude_id: int | None,
) -> list[Complaint]:
    query = db.query(Complaint).filter(
        or_(
            Complaint.product_name == product_name,
            Complaint.batch_number == batch_number,
            Complaint.complaint_type == complaint_type,
        )
    )
    if exclude_id is not None:
        query = query.filter(Complaint.id != exclude_id)
    candidates = {c.id: c for c in query.limit(PREFILTER_LIMIT).all()}

    if description and description.strip():
        try:
            fulltext_query = db.query(Complaint).filter(
                text("MATCH(description) AGAINST(:q IN NATURAL LANGUAGE MODE)")
            ).params(q=description)
            if exclude_id is not None:
                fulltext_query = fulltext_query.filter(Complaint.id != exclude_id)
            for c in fulltext_query.limit(PREFILTER_LIMIT).all():
                candidates[c.id] = c
        except Exception:  # noqa: BLE001 - fulltext is a best-effort widen, not required
            pass

    return list(candidates.values())


def find_duplicates(
    db: Session,
    product_name: str,
    batch_number: str,
    complaint_type: str,
    description: str,
    exclude_id: int | None = None,
) -> list[dict]:
    candidates = _prefilter(db, product_name, batch_number, complaint_type, description, exclude_id)

    scored: list[dict] = []
    for candidate in candidates:
        matched_fields: list[str] = []
        field_bonus = 0.0

        if product_name and candidate.product_name.strip().lower() == product_name.strip().lower():
            matched_fields.append("product_name")
            field_bonus += 30.0
        if batch_number and candidate.batch_number.strip().lower() == batch_number.strip().lower():
            matched_fields.append("batch_number")
            field_bonus += 40.0
        if complaint_type and candidate.complaint_type == complaint_type:
            matched_fields.append("complaint_type")
            field_bonus += 15.0

        text_sim = fuzz.token_sort_ratio(description or "", candidate.description or "")
        if text_sim > 70:
            matched_fields.append("description")

        score = min(100.0, round(0.35 * text_sim + field_bonus, 2))

        if score >= SCORE_THRESHOLD:
            scored.append(
                {
                    "complaint_id": candidate.id,
                    "complaint_number": candidate.complaint_number,
                    "similarity_score": score,
                    "matched_fields": matched_fields,
                    "product_name": candidate.product_name,
                    "batch_number": candidate.batch_number,
                    "complaint_type": candidate.complaint_type,
                    "customer_name": candidate.customer_name,
                    "created_at": candidate.created_at.isoformat(),
                }
            )

    scored.sort(key=lambda d: d["similarity_score"], reverse=True)
    return scored[:MAX_CANDIDATES]
