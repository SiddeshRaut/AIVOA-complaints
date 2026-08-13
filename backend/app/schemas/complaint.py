from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FieldProvenance(BaseModel):
    """Per-field metadata recorded when a value came from AI extraction."""

    value: str | None = None
    confidence: float | None = None
    source: str = "manual"  # "manual" | "ai"


class ComplaintBase(BaseModel):
    complaint_source: str | None = None
    customer_name: str = Field(min_length=1)

    product_name: str = Field(min_length=1)
    product_strength: str | None = None
    batch_number: str = Field(min_length=1)
    manufacturing_date: date | None = None
    expiry_date: date | None = None
    quantity_affected: Decimal | None = None
    quantity_unit: str = "kg"

    complaint_type: str = Field(min_length=1)
    complaint_date: date
    description: str = Field(min_length=1)

    initial_severity: str | None = None
    priority: str | None = None


class ComplaintCreate(ComplaintBase):
    source_document_id: int | None = None
    extraction_metadata: dict | None = None
    ai_severity_suggested: str | None = None
    ai_priority_suggested: str | None = None
    ai_risk_rationale: str | None = None
    acknowledge_duplicates: bool = False


class ComplaintUpdate(BaseModel):
    complaint_source: str | None = None
    customer_name: str | None = None
    product_name: str | None = None
    product_strength: str | None = None
    batch_number: str | None = None
    manufacturing_date: date | None = None
    expiry_date: date | None = None
    quantity_affected: Decimal | None = None
    quantity_unit: str | None = None
    complaint_type: str | None = None
    complaint_date: date | None = None
    description: str | None = None
    initial_severity: str | None = None
    priority: str | None = None
    status: str | None = None


class ComplaintOut(ComplaintBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_number: str
    status: str
    ai_severity_suggested: str | None = None
    ai_priority_suggested: str | None = None
    ai_risk_rationale: str | None = None
    extraction_metadata: dict | None = None
    source_document_id: int | None = None
    created_at: datetime
    updated_at: datetime


class ComplaintListOut(BaseModel):
    items: list[ComplaintOut]
    total: int
