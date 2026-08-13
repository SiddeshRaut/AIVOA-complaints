export interface ExtractedField {
  value: string | null;
  confidence: number;
}

export type ExtractedFieldName =
  | "complaint_source"
  | "customer_name"
  | "product_name"
  | "product_strength"
  | "batch_number"
  | "manufacturing_date"
  | "expiry_date"
  | "quantity_affected"
  | "quantity_unit"
  | "complaint_type"
  | "complaint_date"
  | "description";

export interface DocumentUploadOut {
  document_id: number;
  original_filename: string | null;
  mime_type: string | null;
  source_type: "upload" | "pasted_text";
  text_preview: string;
}

export interface DuplicateCandidate {
  complaint_id: number;
  complaint_number: string;
  similarity_score: number;
  matched_fields: string[];
  product_name: string;
  batch_number: string;
  complaint_type: string;
  customer_name: string;
  created_at: string;
}

export interface RiskClassification {
  severity: string;
  priority: string;
  rationale: string;
}

export interface CompletenessResult {
  missing_required: string[];
  low_confidence: string[];
}

export interface ComplaintCreatePayload {
  complaint_source?: string | null;
  customer_name: string;
  product_name: string;
  product_strength?: string | null;
  batch_number: string;
  manufacturing_date?: string | null;
  expiry_date?: string | null;
  quantity_affected?: number | null;
  quantity_unit: string;
  complaint_type: string;
  complaint_date: string;
  description: string;
  initial_severity?: string | null;
  priority?: string | null;
  source_document_id?: number | null;
  extraction_metadata?: Record<string, ExtractedField> | null;
  ai_severity_suggested?: string | null;
  ai_priority_suggested?: string | null;
  ai_risk_rationale?: string | null;
  acknowledge_duplicates?: boolean;
}

export interface ComplaintOut extends ComplaintCreatePayload {
  id: number;
  complaint_number: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface ComplaintListOut {
  items: ComplaintOut[];
  total: number;
}

export interface DuplicateCheckPayload {
  product_name: string;
  batch_number: string;
  complaint_type: string;
  description: string;
  exclude_id?: number | null;
}

export interface HealthOut {
  status: string;
  db_connected: boolean;
  groq_configured: boolean;
  extraction_model: string;
  chat_model: string;
}

export interface DuplicateConflictDetail {
  message: string;
  duplicates: DuplicateCandidate[];
}
