from datetime import datetime

from sqlalchemy import Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import BIGINT, MEDIUMTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime

from app.database import Base


class ComplaintDocument(Base):
    __tablename__ = "complaint_documents"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    complaint_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True), ForeignKey("complaints.id"), nullable=True
    )

    original_filename: Mapped[str | None] = mapped_column(String(255))
    stored_path: Mapped[str | None] = mapped_column(String(500))
    mime_type: Mapped[str | None] = mapped_column(String(100))
    file_size_bytes: Mapped[int | None] = mapped_column(Integer)
    source_type: Mapped[str] = mapped_column(Enum("upload", "pasted_text", name="source_type_enum"), nullable=False)
    raw_text: Mapped[str | None] = mapped_column(MEDIUMTEXT)

    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    complaint = relationship("Complaint", back_populates="documents", foreign_keys=[complaint_id])
