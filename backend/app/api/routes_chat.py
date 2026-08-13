import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from app.agents.chat_graph import stream_chat_answer
from app.api.deps import get_db
from app.core.exceptions import GroqNotConfiguredError
from app.models.document import ComplaintDocument
from app.schemas.chat import ChatMessageIn

router = APIRouter()


@router.post("/stream")
async def chat_stream(payload: ChatMessageIn, db: Session = Depends(get_db)) -> EventSourceResponse:
    document_text = ""
    if payload.document_id:
        doc = db.get(ComplaintDocument, payload.document_id)
        if doc:
            document_text = doc.raw_text or ""

    async def event_generator():
        try:
            async for token in stream_chat_answer(
                message=payload.message,
                document_text=document_text,
                form_snapshot=payload.form_snapshot,
                history=payload.history,
            ):
                yield {"event": "token", "data": json.dumps({"token": token})}
        except GroqNotConfiguredError as exc:
            yield {"event": "error", "data": json.dumps({"message": str(exc)})}
            return
        except Exception as exc:  # noqa: BLE001
            yield {"event": "error", "data": json.dumps({"message": f"Chat failed: {exc}"})}
            return

        yield {"event": "done", "data": json.dumps({})}

    return EventSourceResponse(event_generator())
