import pytest

from app.core.exceptions import DocumentParseError
from app.services.file_parser import extract_text, guess_kind, parse_eml, parse_txt


def test_guess_kind_by_extension():
    assert guess_kind("complaint.pdf", None) == "pdf"
    assert guess_kind("complaint.docx", None) == "docx"
    assert guess_kind("complaint.eml", None) == "eml"
    assert guess_kind("complaint.txt", None) == "txt"


def test_guess_kind_unsupported_raises():
    with pytest.raises(DocumentParseError):
        guess_kind("complaint.xyz", "application/octet-stream")


def test_parse_txt_utf8():
    assert parse_txt("Batch MET-2026-0112 defect".encode("utf-8")) == "Batch MET-2026-0112 defect"


def test_parse_txt_latin1_fallback():
    data = "café".encode("latin-1")
    assert parse_txt(data) == "café"


def test_parse_eml_extracts_headers_and_body():
    raw = (
        b"From: qa@example.com\r\n"
        b"Subject: Complaint - Batch 123\r\n"
        b"Content-Type: text/plain; charset=utf-8\r\n"
        b"\r\n"
        b"Tablets showed discoloration.\r\n"
    )
    text = parse_eml(raw)
    assert "From: qa@example.com" in text
    assert "Subject: Complaint - Batch 123" in text
    assert "Tablets showed discoloration." in text


def test_extract_text_empty_document_raises():
    with pytest.raises(DocumentParseError):
        extract_text("empty.txt", "text/plain", b"   \n  ")
