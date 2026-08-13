import { useCallback, useRef } from "react";
import { useAppDispatch } from "../../app/hooks";
import type { ComplaintFormFields } from "../complaintForm/complaintFormSlice";
import { setAIRiskSuggestion, setFieldFromAI } from "../complaintForm/complaintFormSlice";
import { checkFinished } from "../duplicates/duplicatesSlice";
import {
  extractionCompleteness,
  extractionDone,
  extractionFailed,
  extractionProgress,
  extractionStarted,
  extractionWarning,
} from "./aiAssistantSlice";

/** EventSource-based hook for GET /api/extraction/stream/{document_id}.
 * EventSource is used (over fetch+ReadableStream) because this is a simple
 * GET-by-id flow with no request body — it gets built-in reconnect for free.
 */
export function useExtractionStream() {
  const dispatch = useAppDispatch();
  const esRef = useRef<EventSource | null>(null);

  const start = useCallback(
    (documentId: number) => {
      esRef.current?.close();
      dispatch(extractionStarted());

      const es = new EventSource(`/api/extraction/stream/${documentId}`);
      esRef.current = es;

      es.addEventListener("progress", (e) => {
        const data = JSON.parse((e as MessageEvent).data);
        dispatch(extractionProgress({ percent: data.percent, message: data.message }));
      });

      es.addEventListener("field", (e) => {
        const data = JSON.parse((e as MessageEvent).data);
        dispatch(extractionProgress({ percent: data.percent }));
        if (data.value) {
          dispatch(
            setFieldFromAI({
              name: data.field as keyof ComplaintFormFields,
              value: data.value,
              confidence: data.confidence,
            })
          );
        }
      });

      es.addEventListener("completeness", (e) => {
        const data = JSON.parse((e as MessageEvent).data);
        dispatch(
          extractionCompleteness({ missingRequired: data.missing_required, lowConfidence: data.low_confidence })
        );
      });

      es.addEventListener("risk", (e) => {
        const data = JSON.parse((e as MessageEvent).data);
        dispatch(setAIRiskSuggestion({ severity: data.severity, priority: data.priority, rationale: data.rationale }));
      });

      es.addEventListener("duplicates", (e) => {
        const data = JSON.parse((e as MessageEvent).data);
        dispatch(checkFinished(data.candidates ?? []));
      });

      es.addEventListener("warning", (e) => {
        const data = JSON.parse((e as MessageEvent).data);
        dispatch(extractionWarning(data.message));
      });

      es.addEventListener("done", () => {
        dispatch(extractionDone());
        es.close();
      });

      // The server's `event: error` frames and native connection-level errors
      // both surface as EventSource "error" events; only the former carries `.data`.
      es.addEventListener("error", (e) => {
        const msgEvent = e as MessageEvent;
        if (msgEvent.data) {
          try {
            const data = JSON.parse(msgEvent.data);
            dispatch(extractionFailed(data.message || "Extraction failed"));
          } catch {
            dispatch(extractionFailed("Extraction failed"));
          }
        } else {
          dispatch(extractionFailed("Connection to extraction stream was lost"));
        }
        es.close();
      });
    },
    [dispatch]
  );

  const stop = useCallback(() => {
    esRef.current?.close();
  }, []);

  return { start, stop };
}
