CHAT_SYSTEM_PROMPT = """You are the AI Complaint Intake Assistant embedded in a pharmaceutical QMS \
complaint-logging tool. Answer the QA user's questions using ONLY the provided source document text \
and the current complaint form data below. Be concise and factual.

If the answer isn't supported by the provided context, say so plainly rather than guessing — this is a \
regulated quality system and fabricated answers are unacceptable. You are not a substitute for a licensed \
QA reviewer's judgment; for severity/CAPA/regulatory decisions, note that a human should confirm.
"""


def build_chat_context(document_text: str, form_snapshot: dict | None) -> str:
    parts = []
    if document_text:
        parts.append(f"SOURCE DOCUMENT:\n{document_text}")
    if form_snapshot:
        form_lines = "\n".join(f"- {k}: {v}" for k, v in form_snapshot.items() if v)
        parts.append(f"CURRENT COMPLAINT FORM DATA:\n{form_lines}")
    return "\n\n".join(parts) if parts else "(No document or form data available yet.)"
