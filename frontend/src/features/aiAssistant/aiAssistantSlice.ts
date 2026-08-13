import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

export type UploadStatus = "idle" | "uploading" | "uploaded" | "error";
export type ExtractionStatus = "idle" | "extracting" | "done" | "error";

export interface AIAssistantState {
  uploadStatus: UploadStatus;
  documentId: number | null;
  documentName: string | null;
  extractionStatus: ExtractionStatus;
  progressPercent: number;
  progressMessage: string;
  error: string | null;
  warnings: string[];
  completeness: { missingRequired: string[]; lowConfidence: string[] } | null;
}

const initialState: AIAssistantState = {
  uploadStatus: "idle",
  documentId: null,
  documentName: null,
  extractionStatus: "idle",
  progressPercent: 0,
  progressMessage: "",
  error: null,
  warnings: [],
  completeness: null,
};

const aiAssistantSlice = createSlice({
  name: "aiAssistant",
  initialState,
  reducers: {
    uploadStarted(state) {
      state.uploadStatus = "uploading";
      state.error = null;
    },
    uploadSucceeded(state, action: PayloadAction<{ documentId: number; documentName: string | null }>) {
      state.uploadStatus = "uploaded";
      state.documentId = action.payload.documentId;
      state.documentName = action.payload.documentName;
    },
    uploadFailed(state, action: PayloadAction<string>) {
      state.uploadStatus = "error";
      state.error = action.payload;
    },
    extractionStarted(state) {
      state.extractionStatus = "extracting";
      state.progressPercent = 0;
      state.progressMessage = "Starting extraction...";
      state.error = null;
      state.warnings = [];
      state.completeness = null;
    },
    extractionProgress(state, action: PayloadAction<{ percent: number; message?: string }>) {
      state.progressPercent = action.payload.percent;
      if (action.payload.message) state.progressMessage = action.payload.message;
    },
    extractionCompleteness(
      state,
      action: PayloadAction<{ missingRequired: string[]; lowConfidence: string[] }>
    ) {
      state.completeness = action.payload;
    },
    extractionWarning(state, action: PayloadAction<string>) {
      state.warnings.push(action.payload);
    },
    extractionDone(state) {
      state.extractionStatus = "done";
      state.progressPercent = 100;
      state.progressMessage = "Extraction complete.";
    },
    extractionFailed(state, action: PayloadAction<string>) {
      state.extractionStatus = "error";
      state.error = action.payload;
    },
    resetAssistant() {
      return { ...initialState };
    },
  },
});

export const {
  uploadStarted,
  uploadSucceeded,
  uploadFailed,
  extractionStarted,
  extractionProgress,
  extractionCompleteness,
  extractionWarning,
  extractionDone,
  extractionFailed,
  resetAssistant,
} = aiAssistantSlice.actions;
export default aiAssistantSlice.reducer;
