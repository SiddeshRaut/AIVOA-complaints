import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatState {
  messages: ChatMessage[];
  isStreaming: boolean;
  error: string | null;
}

const initialState: ChatState = {
  messages: [],
  isStreaming: false,
  error: null,
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    userMessageSent(state, action: PayloadAction<string>) {
      state.messages.push({ role: "user", content: action.payload });
      state.messages.push({ role: "assistant", content: "" });
      state.isStreaming = true;
      state.error = null;
    },
    assistantTokenReceived(state, action: PayloadAction<string>) {
      const last = state.messages[state.messages.length - 1];
      if (last && last.role === "assistant") {
        last.content += action.payload;
      }
    },
    streamFinished(state) {
      state.isStreaming = false;
    },
    streamFailed(state, action: PayloadAction<string>) {
      state.isStreaming = false;
      state.error = action.payload;
      const last = state.messages[state.messages.length - 1];
      if (last && last.role === "assistant" && !last.content) {
        last.content = `(error: ${action.payload})`;
      }
    },
    resetChat() {
      return { ...initialState };
    },
  },
});

export const { userMessageSent, assistantTokenReceived, streamFinished, streamFailed, resetChat } =
  chatSlice.actions;
export default chatSlice.reducer;
