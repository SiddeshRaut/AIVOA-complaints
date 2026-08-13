import { useCallback, useRef } from "react";
import { useAppDispatch } from "../../app/hooks";
import { assistantTokenReceived, streamFailed, streamFinished, userMessageSent } from "./chatSlice";

function parseSSEBlock(block: string): { event: string; data: string } {
  let event = "message";
  const dataLines: string[] = [];
  for (const line of block.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
  }
  return { event, data: dataLines.join("\n") };
}

/** fetch + ReadableStream (not EventSource) because chat needs a POST body
 * (message + document/form context) — EventSource only supports GET.
 */
export function useChatStream() {
  const dispatch = useAppDispatch();
  const abortRef = useRef<AbortController | null>(null);

  const send = useCallback(
    async (
      message: string,
      documentId: number | null,
      formSnapshot: Record<string, string>,
      history: { role: string; content: string }[]
    ) => {
      dispatch(userMessageSent(message));
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      try {
        const res = await fetch("/api/chat/stream", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message, document_id: documentId, form_snapshot: formSnapshot, history }),
          signal: controller.signal,
        });

        if (!res.ok || !res.body) {
          throw new Error(`Chat request failed (${res.status})`);
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          // sse-starlette frames events with CRLF; normalize to LF so the "\n\n"
          // block separator below matches regardless of the server's line endings.
          buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n");

          let sepIndex: number;
          while ((sepIndex = buffer.indexOf("\n\n")) !== -1) {
            const rawEvent = buffer.slice(0, sepIndex);
            buffer = buffer.slice(sepIndex + 2);
            const { event, data } = parseSSEBlock(rawEvent);

            if (event === "token" && data) {
              dispatch(assistantTokenReceived(JSON.parse(data).token));
            } else if (event === "error" && data) {
              dispatch(streamFailed(JSON.parse(data).message || "Chat failed"));
              return;
            } else if (event === "done") {
              dispatch(streamFinished());
              return;
            }
          }
        }
        dispatch(streamFinished());
      } catch (err) {
        if ((err as Error).name === "AbortError") return;
        dispatch(streamFailed((err as Error).message || "Chat failed"));
      }
    },
    [dispatch]
  );

  return { send };
}
