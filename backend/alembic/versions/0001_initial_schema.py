"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-08-13

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "complaints",
        sa.Column("id", mysql.BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        sa.Column("complaint_number", sa.String(32), nullable=False, unique=True),
        sa.Column("complaint_source", sa.String(50), nullable=True),
        sa.Column("customer_name", sa.String(255), nullable=False),
        sa.Column("product_name", sa.String(255), nullable=False),
        sa.Column("product_strength", sa.String(100), nullable=True),
        sa.Column("batch_number", sa.String(100), nullable=False),
        sa.Column("manufacturing_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("quantity_affected", sa.Numeric(12, 3), nullable=True),
        sa.Column("quantity_unit", sa.String(20), nullable=False, server_default="kg"),
        sa.Column("complaint_type", sa.String(50), nullable=False),
        sa.Column("complaint_date", sa.Date(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("initial_severity", sa.String(20), nullable=True),
        sa.Column("priority", sa.String(20), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="Pending Triage"),
        sa.Column("ai_severity_suggested", sa.String(20), nullable=True),
        sa.Column("ai_priority_suggested", sa.String(20), nullable=True),
        sa.Column("ai_risk_rationale", sa.Text(), nullable=True),
        sa.Column("extraction_metadata", sa.JSON(), nullable=True),
        sa.Column("source_document_id", mysql.BIGINT(unsigned=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_product_batch", "complaints", ["product_name", "batch_number"])
    op.create_index("idx_complaint_type", "complaints", ["complaint_type"])
    op.create_index("idx_created_at", "complaints", ["created_at"])
    op.execute(
        "ALTER TABLE complaints ADD FULLTEXT INDEX ftx_description (description)"
    )

    op.create_table(
        "complaint_documents",
        sa.Column("id", mysql.BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        sa.Column(
            "complaint_id",
            mysql.BIGINT(unsigned=True),
            sa.ForeignKey("complaints.id"),
            nullable=True,
        ),
        sa.Column("original_filename", sa.String(255), nullable=True),
        sa.Column("stored_path", sa.String(500), nullable=True),
        sa.Column("mime_type", sa.String(100), nullable=True),
        sa.Column("file_size_bytes", sa.Integer(), nullable=True),
        sa.Column(
            "source_type",
            sa.Enum("upload", "pasted_text", name="source_type_enum"),
            nullable=False,
        ),
        sa.Column("raw_text", mysql.MEDIUMTEXT(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        mysql_engine="InnoDB",
    )

    op.create_table(
        "duplicate_matches",
        sa.Column("id", mysql.BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        sa.Column(
            "complaint_id",
            mysql.BIGINT(unsigned=True),
            sa.ForeignKey("complaints.id"),
            nullable=False,
        ),
        sa.Column(
            "matched_complaint_id",
            mysql.BIGINT(unsigned=True),
            sa.ForeignKey("complaints.id"),
            nullable=False,
        ),
        sa.Column("similarity_score", sa.Numeric(5, 2), nullable=False),
        sa.Column("matched_fields", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        mysql_engine="InnoDB",
    )

    op.create_table(
        "audit_log",
        sa.Column("id", mysql.BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        sa.Column(
            "complaint_id",
            mysql.BIGINT(unsigned=True),
            sa.ForeignKey("complaints.id"),
            nullable=True,
        ),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("actor", sa.String(100), nullable=False, server_default="system"),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        mysql_engine="InnoDB",
    )

    op.create_table(
        "chat_messages",
        sa.Column("id", mysql.BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        sa.Column(
            "complaint_id",
            mysql.BIGINT(unsigned=True),
            sa.ForeignKey("complaints.id"),
            nullable=True,
        ),
        sa.Column("role", sa.Enum("user", "assistant", name="chat_role_enum"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        mysql_engine="InnoDB",
    )


def downgrade() -> None:
    op.drop_table("chat_messages")
    op.drop_table("audit_log")
    op.drop_table("duplicate_matches")
    op.drop_table("complaint_documents")
    op.drop_table("complaints")
