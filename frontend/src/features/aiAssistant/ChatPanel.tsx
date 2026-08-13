import { useState } from "react";
import { useAppSelector } from "../../app/hooks";
import { Button } from "../../components/ui/Button";
import { useChatStream } from "./useChatStream";

export default function ChatPanel() {
  const { messages, isStreaming } = useAppSelector((s) => s.chat);
  const documentId = useAppSelector((s) => s.aiAssistant.documentId);
  const fields = useAppSelector((s) => s.complaintForm.fields);
  const { send } = useChatStream();
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim() || isStreaming) return;
    const history = messages.map((m) => ({ role: m.role, content: m.content }));
    send(input, documentId, { ...fields }, history);
    setInput("");
  };

  return (
    <div className="mt-5 rounded-xl border border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-4 py-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
        AI Assistant
      </div>

      <div className="max-h-64 space-y-3 overflow-y-auto px-4 py-3">
        {messages.length === 0 ? (
          <div className="flex items-start gap-2 rounded-lg bg-brand-50 px-3 py-2 text-sm text-brand-800">
            <span>🤖</span>
            <span>
              Upload a complaint document or paste text above. I will automatically extract the details and
              populate the form for you.
            </span>
          </div>
        ) : (
          messages.map((m, i) => (
            <div
              key={i}
              className={`rounded-lg px-3 py-2 text-sm ${
                m.role === "user" ? "ml-8 bg-slate-100 text-slate-800" : "mr-8 bg-brand-50 text-brand-900"
              }`}
            >
              {m.content || (isStreaming && i === messages.length - 1 ? "…" : "")}
            </div>
          ))
        )}
      </div>

      <div className="border-t border-slate-200 p-3">
        <div className="flex gap-2">
          <input
            className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/30"
            placeholder="Ask me anything about this complaint..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <Button variant="primary" onClick={handleSend} disabled={isStreaming} type="button">
            ➤
          </Button>
        </div>
        <p className="mt-2 text-center text-[11px] text-slate-400">
          AI responses may contain errors. Please verify information.
        </p>
      </div>
    </div>
  );
}
