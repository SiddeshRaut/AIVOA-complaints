import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { DuplicateCandidate } from "../../api/types";

export interface DuplicatesState {
  candidates: DuplicateCandidate[];
  isChecking: boolean;
  modalOpen: boolean;
}

const initialState: DuplicatesState = {
  candidates: [],
  isChecking: false,
  modalOpen: false,
};

const duplicatesSlice = createSlice({
  name: "duplicates",
  initialState,
  reducers: {
    checkStarted(state) {
      state.isChecking = true;
    },
    checkFinished(state, action: PayloadAction<DuplicateCandidate[]>) {
      state.isChecking = false;
      state.candidates = action.payload;
    },
    openModal(state) {
      state.modalOpen = true;
    },
    closeModal(state) {
      state.modalOpen = false;
    },
    clearDuplicates(state) {
      state.candidates = [];
      state.modalOpen = false;
    },
  },
});

export const { checkStarted, checkFinished, openModal, closeModal, clearDuplicates } =
  duplicatesSlice.actions;
export default duplicatesSlice.reducer;
