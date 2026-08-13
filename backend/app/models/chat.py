from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    complaint_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True), ForeignKey("complaints.id"), nullable=True
    )
    role: Mapped[str] = mapped_column(Enum("user", "assistant", name="chat_role_enum"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    complaint = relationship("Complaint", back_populates="chat_messages")
