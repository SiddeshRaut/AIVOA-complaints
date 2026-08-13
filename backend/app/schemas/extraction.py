from pydantic import BaseModel, Field


class ExtractedField(BaseModel):
    value: str | None = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)


class ExtractedComplaintFields(BaseModel):
    """Structured output the LLM must produce for the complaint form fields."""

    complaint_source: ExtractedField = ExtractedField()
    customer_name: ExtractedField = ExtractedField()
    product_name: ExtractedField = ExtractedField()
    product_strength: ExtractedField = ExtractedField()
    batch_number: ExtractedField = ExtractedField()
    manufacturing_date: ExtractedField = ExtractedField()
    expiry_date: ExtractedField = ExtractedField()
    quantity_affected: ExtractedField = ExtractedField()
    quantity_unit: ExtractedField = ExtractedField()
    complaint_type: ExtractedField = ExtractedField()
    complaint_date: ExtractedField = ExtractedField()
    description: ExtractedField = ExtractedField()


class DocumentUploadOut(BaseModel):
    document_id: int
    original_filename: str | None = None
    mime_type: str | None = None
    source_type: str
    text_preview: str


class PasteTextIn(BaseModel):
    text: str = Field(min_length=1)


class RiskClassification(BaseModel):
    severity: str
    priority: str
    rationale: str


class CompletenessResult(BaseModel):
    missing_required: list[str]
    low_confidence: list[str]


class DuplicateCandidate(BaseModel):
    complaint_id: int
    complaint_number: str
    similarity_score: float
    matched_fields: list[str]
    product_name: str
    batch_number: str
    complaint_type: str
    customer_name: str
    created_at: str


class ExtractionResult(BaseModel):
    document_id: int
    fields: ExtractedComplaintFields
    completeness: CompletenessResult
    risk: RiskClassification | None = None
    duplicates: list[DuplicateCandidate] = []
    warnings: list[str] = []
