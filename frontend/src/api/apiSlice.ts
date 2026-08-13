import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type {
  ComplaintCreatePayload,
  ComplaintListOut,
  ComplaintOut,
  DocumentUploadOut,
  DuplicateCandidate,
  DuplicateCheckPayload,
  HealthOut,
} from "./types";

export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  tagTypes: ["Complaint"],
  endpoints: (builder) => ({
    uploadDocument: builder.mutation<DocumentUploadOut, FormData>({
      query: (formData) => ({ url: "/documents/upload", method: "POST", body: formData }),
    }),
    pasteDocument: builder.mutation<DocumentUploadOut, { text: string }>({
      query: (body) => ({ url: "/documents/paste", method: "POST", body }),
    }),
    createComplaint: builder.mutation<ComplaintOut, ComplaintCreatePayload>({
      query: (body) => ({ url: "/complaints", method: "POST", body }),
      invalidatesTags: ["Complaint"],
    }),
    listComplaints: builder.query<ComplaintListOut, { skip?: number; limit?: number } | void>({
      query: (params) => ({ url: "/complaints", params: params ?? undefined }),
      providesTags: ["Complaint"],
    }),
    checkDuplicates: builder.mutation<DuplicateCandidate[], DuplicateCheckPayload>({
      query: (body) => ({ url: "/complaints/check-duplicates", method: "POST", body }),
    }),
    getHealth: builder.query<HealthOut, void>({
      query: () => "/health",
    }),
  }),
});

export const {
  useUploadDocumentMutation,
  usePasteDocumentMutation,
  useCreateComplaintMutation,
  useListComplaintsQuery,
  useCheckDuplicatesMutation,
  useGetHealthQuery,
} = apiSlice;
