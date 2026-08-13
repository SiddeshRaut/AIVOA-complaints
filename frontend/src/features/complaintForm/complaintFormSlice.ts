import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { ExtractedFieldName } from "../../api/types";

export type ComplaintFormFields = {
  complaint_source: string;
  customer_name: string;
  product_name: string;
  product_strength: string;
  batch_number: string;
  manufacturing_date: string;
  expiry_date: string;
  quantity_affected: string;
  quantity_unit: string;
  complaint_type: string;
  complaint_date: string;
  description: string;
  initial_severity: string;
  priority: string;
};

export type FieldSource = "manual" | "ai";

export interface FieldMeta {
  source: FieldSource;
  confidence?: number;
  justUpdated?: boolean;
}

type MetaFieldName = ExtractedFieldName | "initial_severity" | "priority";

export interface ComplaintFormState {
  fields: ComplaintFormFields;
  meta: Record<MetaFieldName, FieldMeta>;
  status: string;
  isDirty: boolean;
  savedComplaintNumber: string | null;
  aiRiskRationale: string | null;
}

const emptyFields: ComplaintFormFields = {
  complaint_source: "",
  customer_name: "",
  product_name: "",
  product_strength: "",
  batch_number: "",
  manufacturing_date: "",
  expiry_date: "",
  quantity_affected: "",
  quantity_unit: "kg",
  complaint_type: "",
  complaint_date: "",
  description: "",
  initial_severity: "",
  priority: "",
};

function freshMeta(): Record<MetaFieldName, FieldMeta> {
  const names: MetaFieldName[] = [
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
    "initial_severity",
    "priority",
  ];
  return Object.fromEntries(names.map((n) => [n, { source: "manual" as FieldSource }])) as Record<
    MetaFieldName,
    FieldMeta
  >;
}

const initialState: ComplaintFormState = {
  fields: { ...emptyFields },
  meta: freshMeta(),
  status: "Pending Triage",
  isDirty: false,
  savedComplaintNumber: null,
  aiRiskRationale: null,
};

const complaintFormSlice = createSlice({
  name: "complaintForm",
  initialState,
  reducers: {
    setField(state, action: PayloadAction<{ name: keyof ComplaintFormFields; value: string }>) {
      const { name, value } = action.payload;
      state.fields[name] = value;
      state.meta[name as MetaFieldName] = { source: "manual" };
      state.isDirty = true;
    },
    setFieldFromAI(
      state,
      action: PayloadAction<{ name: keyof ComplaintFormFields; value: string; confidence: number }>
    ) {
      const { name, value, confidence } = action.payload;
      if (!value) return;
      state.fields[name] = value;
      state.meta[name as MetaFieldName] = { source: "ai", confidence, justUpdated: true };
      state.isDirty = true;
    },
    clearFieldFlash(state, action: PayloadAction<keyof ComplaintFormFields>) {
      const meta = state.meta[action.payload as MetaFieldName];
      if (meta) meta.justUpdated = false;
    },
    setAIRiskSuggestion(
      state,
      action: PayloadAction<{ severity: string; priority: string; rationale: string }>
    ) {
      const { severity, priority, rationale } = action.payload;
      if (!state.fields.initial_severity) {
        state.fields.initial_severity = severity;
        state.meta.initial_severity = { source: "ai", justUpdated: true };
      }
      if (!state.fields.priority) {
        state.fields.priority = priority;
        state.meta.priority = { source: "ai", justUpdated: true };
      }
      state.aiRiskRationale = rationale;
    },
    resetForm() {
      return { ...initialState, fields: { ...emptyFields }, meta: freshMeta() };
    },
    markSaved(state, action: PayloadAction<{ complaintNumber: string; status: string }>) {
      state.savedComplaintNumber = action.payload.complaintNumber;
      state.status = action.payload.status;
      state.isDirty = false;
    },
  },
});

export const { setField, setFieldFromAI, clearFieldFlash, setAIRiskSuggestion, resetForm, markSaved } =
  complaintFormSlice.actions;
export default complaintFormSlice.reducer;
