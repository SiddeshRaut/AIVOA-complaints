from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api import routes_chat, routes_complaints, routes_duplicates, routes_extraction, routes_upload
from app.config import get_settings
from app.core.logging import setup_logging
from app.database import SessionLocal

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(title="AIVOA Complaint Management API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_complaints.router, prefix="/api/complaints", tags=["complaints"])
app.include_router(routes_upload.router, prefix="/api/documents", tags=["documents"])
app.include_router(routes_extraction.router, prefix="/api/extraction", tags=["extraction"])
app.include_router(routes_chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(routes_duplicates.router, prefix="/api/complaints", tags=["duplicates"])


@app.get("/api/health")
def health() -> dict:
    db_connected = True
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception:  # noqa: BLE001
        db_connected = False

    return {
        "status": "ok" if db_connected else "degraded",
        "db_connected": db_connected,
        "groq_configured": settings.groq_configured,
        "extraction_model": settings.groq_extraction_model,
        "chat_model": settings.groq_chat_model,
    }





it config --global user.email "YOUR_GITHUB_EMAIL"

git add .
git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/YOUR_USERNAME/AIVOA-complaints.git

git push -u origin main