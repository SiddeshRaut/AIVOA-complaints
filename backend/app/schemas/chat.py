from pydantic import BaseModel, Field


class ChatMessageIn(BaseModel):
    message: str = Field(min_length=1)
    document_id: int | None = None
    complaint_id: int | None = None
    form_snapshot: dict | None = None
    history: list[dict] = []
