from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import JSON, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    complaint_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    complaint_source: Mapped[str | None] = mapped_column(String(50))
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)

    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_strength: Mapped[str | None] = mapped_column(String(100))
    batch_number: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturing_date: Mapped[date | None] = mapped_column(Date)
    expiry_date: Mapped[date | None] = mapped_column(Date)
    quantity_affected: Mapped[Decimal | None] = mapped_column(Numeric(12, 3))
    quantity_unit: Mapped[str] = mapped_column(String(20), default="kg", server_default="kg")

    complaint_type: Mapped[str] = mapped_column(String(50), nullable=False)
    complaint_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    initial_severity: Mapped[str | None] = mapped_column(String(20))
    priority: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), default="Pending Triage", server_default="Pending Triage")

    ai_severity_suggested: Mapped[str | None] = mapped_column(String(20))
    ai_priority_suggested: Mapped[str | None] = mapped_column(String(20))
    ai_risk_rationale: Mapped[str | None] = mapped_column(Text)

    extraction_metadata: Mapped[dict | None] = mapped_column(JSON)
    source_document_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    documents = relationship("ComplaintDocument", back_populates="complaint", foreign_keys="ComplaintDocument.complaint_id")
    chat_messages = relationship("ChatMessage", back_populates="complaint")


class DuplicateMatch(Base):
    __tablename__ = "duplicate_matches"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    complaint_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), nullable=False)
    matched_complaint_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), nullable=False)
    similarity_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    matched_fields: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    complaint_id: Mapped[int | None] = mapped_column(BIGINT(unsigned=True), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    actor: Mapped[str] = mapped_column(String(100), default="system", server_default="system")
    details: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
