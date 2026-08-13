import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from app.agents.extraction_graph import build_extraction_graph
from app.api.deps import get_db
from app.models.document import ComplaintDocument
from app.schemas.extraction import (
    CompletenessResult,
    ExtractedComplaintFields,
    ExtractionResult,
    RiskClassification,
)

router = APIRouter()

# Order fields are revealed in the SSE stream, matching the form's visual section order.
FIELD_EMIT_ORDER = [
    "complaint_source",
    "customer_name",
    "product_name",
    "product_strength",
    "batch_number",
    "manufacturing_date",
    "expiry_date",
    "quantity_affected",
    "quantity_unit",
    "complaint_type",
    "complaint_date",
    "description",
]


class ExtractionRunIn(BaseModel):
    document_id: int


def _get_document_text(db: Session, document_id: int) -> str:
    doc = db.get(ComplaintDocument, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc.raw_text or ""


def _run_graph(db: Session, document_id: int, document_text: str) -> dict:
    graph = build_extraction_graph(db)
    return graph.invoke({"document_id": document_id, "document_text": document_text})


def _build_result(document_id: int, final_state: dict) -> ExtractionResult:
    return ExtractionResult(
        document_id=document_id,
        fields=ExtractedComplaintFields.model_validate(final_state.get("extracted_fields", {})),
        completeness=CompletenessResult(
            missing_required=final_state.get("missing_required_fields", []),
            low_confidence=final_state.get("low_confidence_fields", []),
        ),
        risk=(
            RiskClassification(
                severity=final_state["risk_severity"],
                priority=final_state["risk_priority"],
                rationale=final_state["risk_rationale"],
            )
            if final_state.get("risk_severity")
            else None
        ),
        duplicates=final_state.get("duplicate_candidates", []),
        warnings=final_state.get("warnings", []),
    )


@router.post("/run", response_model=ExtractionResult)
def run_extraction(payload: ExtractionRunIn, db: Session = Depends(get_db)) -> ExtractionResult:
    document_text = _get_document_text(db, payload.document_id)
    final_state = _run_graph(db, payload.document_id, document_text)
    return _build_result(payload.document_id, final_state)


@router.get("/stream/{document_id}")
async def stream_extraction(document_id: int, db: Session = Depends(get_db)) -> EventSourceResponse:
    document_text = _get_document_text(db, document_id)

    async def event_generator():
        yield {"event": "progress", "data": json.dumps({"percent": 10, "message": "Parsing document..."})}
        await asyncio.sleep(0.2)
        yield {
            "event": "progress",
            "data": json.dumps(
                {"percent": 30, "message": "Analyzing document content and extracting key details..."}
            ),
        }

        try:
            final_state = await asyncio.to_thread(_run_graph, db, document_id, document_text)
        except Exception as exc:  # noqa: BLE001
            yield {"event": "error", "data": json.dumps({"message": str(exc)})}
            return

        fields = final_state.get("extracted_fields", {})
        percent = 30
        step = 40 // max(len(FIELD_EMIT_ORDER), 1)
        for name in FIELD_EMIT_ORDER:
            field = fields.get(name, {"value": None, "confidence": 0.0})
            percent = min(70, percent + step)
            yield {
                "event": "field",
                "data": json.dumps(
                    {
                        "field": name,
                        "value": field.get("value"),
                        "confidence": field.get("confidence", 0.0),
                        "percent": percent,
                    }
                ),
            }
            await asyncio.sleep(0.2)

        yield {
            "event": "completeness",
            "data": json.dumps(
                {
                    "missing_required": final_state.get("missing_required_fields", []),
                    "low_confidence": final_state.get("low_confidence_fields", []),
                }
            ),
        }
        await asyncio.sleep(0.15)

        if final_state.get("risk_severity"):
            yield {
                "event": "risk",
                "data": json.dumps(
                    {
                        "severity": final_state["risk_severity"],
                        "priority": final_state["risk_priority"],
                        "rationale": final_state["risk_rationale"],
                    }
                ),
            }
            await asyncio.sleep(0.15)

        yield {
            "event": "duplicates",
            "data": json.dumps({"candidates": final_state.get("duplicate_candidates", [])}),
        }

        for warning in final_state.get("warnings", []):
            yield {"event": "warning", "data": json.dumps({"message": warning})}

        yield {"event": "done", "data": json.dumps({"percent": 100})}

    return EventSourceResponse(event_generator())
