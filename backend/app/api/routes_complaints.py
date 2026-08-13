from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.complaint import AuditLog, Complaint, DuplicateMatch
from app.schemas.complaint import ComplaintCreate, ComplaintListOut, ComplaintOut, ComplaintUpdate
from app.services.complaint_number import format_complaint_number
from app.services.duplicate_service import find_duplicates

router = APIRouter()


@router.post("", response_model=ComplaintOut, status_code=201)
def create_complaint(payload: ComplaintCreate, db: Session = Depends(get_db)) -> Complaint:
    if not payload.acknowledge_duplicates:
        duplicates = find_duplicates(
            db,
            product_name=payload.product_name,
            batch_number=payload.batch_number,
            complaint_type=payload.complaint_type,
            description=payload.description,
        )
        if duplicates:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Possible duplicate complaint(s) found. Resubmit with acknowledge_duplicates=true to save anyway.",
                    "duplicates": duplicates,
                },
            )

    complaint = Complaint(
        complaint_number="PENDING",
        complaint_source=payload.complaint_source,
        customer_name=payload.customer_name,
        product_name=payload.product_name,
        product_strength=payload.product_strength,
        batch_number=payload.batch_number,
        manufacturing_date=payload.manufacturing_date,
        expiry_date=payload.expiry_date,
        quantity_affected=payload.quantity_affected,
        quantity_unit=payload.quantity_unit,
        complaint_type=payload.complaint_type,
        complaint_date=payload.complaint_date,
        description=payload.description,
        initial_severity=payload.initial_severity,
        priority=payload.priority,
        source_document_id=payload.source_document_id,
        extraction_metadata=payload.extraction_metadata,
        ai_severity_suggested=payload.ai_severity_suggested,
        ai_priority_suggested=payload.ai_priority_suggested,
        ai_risk_rationale=payload.ai_risk_rationale,
    )
    db.add(complaint)
    db.flush()  # assigns complaint.id

    complaint.complaint_number = format_complaint_number(complaint.id)

    db.add(
        AuditLog(
            complaint_id=complaint.id,
            action="created",
            details={"source_document_id": payload.source_document_id},
        )
    )

    if payload.acknowledge_duplicates:
        duplicates = find_duplicates(
            db,
            product_name=payload.product_name,
            batch_number=payload.batch_number,
            complaint_type=payload.complaint_type,
            description=payload.description,
            exclude_id=complaint.id,
        )
        for dup in duplicates:
            db.add(
                DuplicateMatch(
                    complaint_id=complaint.id,
                    matched_complaint_id=dup["complaint_id"],
                    similarity_score=dup["similarity_score"],
                    matched_fields=dup["matched_fields"],
                )
            )
        if duplicates:
            db.add(
                AuditLog(
                    complaint_id=complaint.id,
                    action="duplicate_flagged",
                    details={"candidates": duplicates},
                )
            )

    db.commit()
    db.refresh(complaint)
    return complaint


@router.get("", response_model=ComplaintListOut)
def list_complaints(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> dict:
    total = db.query(Complaint).count()
    items = (
        db.query(Complaint)
        .order_by(desc(Complaint.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {"items": items, "total": total}


@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)) -> Complaint:
    complaint = db.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@router.patch("/{complaint_id}", response_model=ComplaintOut)
def update_complaint(complaint_id: int, payload: ComplaintUpdate, db: Session = Depends(get_db)) -> Complaint:
    complaint = db.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(complaint, field, value)

    db.add(AuditLog(complaint_id=complaint.id, action="updated", details=updates))
    db.commit()
    db.refresh(complaint)
    return complaint
