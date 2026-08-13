import { configureStore } from "@reduxjs/toolkit";
import { apiSlice } from "../api/apiSlice";
import complaintFormReducer from "../features/complaintForm/complaintFormSlice";
import aiAssistantReducer from "../features/aiAssistant/aiAssistantSlice";
import chatReducer from "../features/aiAssistant/chatSlice";
import duplicatesReducer from "../features/duplicates/duplicatesSlice";

export const store = configureStore({
  reducer: {
    complaintForm: complaintFormReducer,
    aiAssistant: aiAssistantReducer,
    chat: chatReducer,
    duplicates: duplicatesReducer,
    [apiSlice.reducerPath]: apiSlice.reducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(apiSlice.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
