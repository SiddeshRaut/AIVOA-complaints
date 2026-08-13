from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.config import get_settings
from app.core.exceptions import DocumentParseError
from app.models.document import ComplaintDocument
from app.schemas.extraction import DocumentUploadOut, PasteTextIn
from app.services.file_parser import extract_text
from app.services.storage import save_upload

router = APIRouter()
settings = get_settings()


@router.post("/upload", response_model=DocumentUploadOut)
async def upload_document(file: UploadFile, db: Session = Depends(get_db)) -> dict:
    data = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.max_upload_size_mb}MB limit")

    try:
        text = extract_text(file.filename or "upload", file.content_type, data)
    except DocumentParseError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    stored_path = save_upload(file.filename or "upload", data)

    doc = ComplaintDocument(
        original_filename=file.filename,
        stored_path=stored_path,
        mime_type=file.content_type,
        file_size_bytes=len(data),
        source_type="upload",
        raw_text=text,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "document_id": doc.id,
        "original_filename": doc.original_filename,
        "mime_type": doc.mime_type,
        "source_type": doc.source_type,
        "text_preview": text[:500],
    }


@router.post("/paste", response_model=DocumentUploadOut)
def paste_document(payload: PasteTextIn, db: Session = Depends(get_db)) -> dict:
    doc = ComplaintDocument(
        original_filename=None,
        stored_path=None,
        mime_type="text/plain",
        file_size_bytes=len(payload.text.encode("utf-8")),
        source_type="pasted_text",
        raw_text=payload.text,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "document_id": doc.id,
        "original_filename": None,
        "mime_type": doc.mime_type,
        "source_type": doc.source_type,
        "text_preview": payload.text[:500],
    }
