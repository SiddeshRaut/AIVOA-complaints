# AIVOA Complaint Management System

An AI-powered Customer Complaint Management System for pharmaceutical (API/FDF)
manufacturing quality assurance. Upload or paste a complaint document, watch an
AI agent extract structured fields into the complaint form field-by-field, review
AI-flagged completeness/risk/duplicate warnings, and chat with an assistant
grounded in the source document.

Built for the AIVOA.AI Round 1 AI Product Engineer take-home assignment.

## Stack

- **Frontend**: React + Redux Toolkit (RTK Query), Vite, TypeScript, Tailwind CSS, Google Inter
- **Backend**: FastAPI, SQLAlchemy + Alembic
- **AI agent framework**: LangGraph (extraction graph + chat graph)
- **LLM**: Groq — `llama-3.1-8b-instant` for extraction, `llama-3.3-70b-versatile` for risk classification and chat
  (the assignment brief specifies `gemma2-9b-it`, but Groq has since decommissioned that model — the extraction
  model is fully configurable via `GROQ_EXTRACTION_MODEL` in `.env` if you want to swap it back or try another)
- **Database**: MySQL 8
- **Orchestration**: Docker Compose (one command starts everything)

## Bonus AI features implemented

1. **Complaint Completeness Checker** — flags missing required fields and low-confidence extracted values after extraction.
2. **AI Risk Classification** — suggests Initial Severity (Critical/Major/Minor) and Priority (High/Medium/Low) with a rationale.
3. **Duplicate Complaint Detection** — SQL prefilter + fuzzy-matching (rapidfuzz) against existing complaints, both during extraction and again right before Save, with a warning modal.

## Quick start

1. Copy `.env.example` to `.env` and fill in a Groq API key from [console.groq.com/keys](https://console.groq.com/keys):

   ```bash
   cp .env.example .env
   ```

   The app runs fine without a key too — AI features degrade gracefully (manual
   complaint entry, completeness/risk/duplicate features just won't populate),
   and `/api/health` reports whether a key is configured.

2. Start everything:

   ```bash
   docker compose up --build
   ```

3. Seed demo data (10 sample complaints, including two intentional near-duplicate
   pairs for demoing Duplicate Detection):

   ```bash
   docker compose exec backend python -m scripts.seed_db
   ```

4. Open the app: **http://localhost:5173**

   Backend API docs (Swagger UI): **http://localhost:8000/docs**

## Demoing the AI flow

Sample pharma complaint documents are in [`sample_data/documents/`](sample_data/documents/)
(PDF, DOCX, TXT, EML) — drag one into the AI Complaint Intake Assistant panel, or
use "Paste Complaint Text / Email" and paste in any of the `.txt`/`.eml` contents.

- `complaint_02_insulin_particulate.eml` and `complaint_03_paracetamol_cracked.docx`
  match seeded complaints on product + batch number — uploading either (with a
  Groq key configured) and saving will trigger the duplicate-warning modal.
- `complaint_01_ibuprofen_discoloration.txt`, `complaint_04_azithromycin_adverse_event.pdf`,
  and `complaint_05_metformin_counterfeit.txt` are fresh products for a clean
  extraction-to-save walkthrough.

## Architecture notes

- **Extraction pipeline** (`backend/app/agents/extraction_graph.py`): a LangGraph
  `StateGraph` — `preprocess_document → extract_fields → completeness_check →
  risk_classification → duplicate_check`. `extract_fields` uses strict JSON-schema
  prompting + Pydantic validation with a bounded retry loop (small/fast Groq models don't
  reliably support native tool-calling on Groq). The "fields fill in one at a time"
  effect in the UI is the API staggering emission of the already-complete result
  as SSE events, not literal token-level extraction — this keeps LLM calls at
  exactly 2 per document (extraction + risk) and is friendlier to Groq's free tier.
- **Chat** (`backend/app/agents/chat_graph.py`): a second LangGraph graph
  (`retrieve_context → generate_answer`) streamed via `astream_events`, which is
  genuine token-level streaming (unlike the staggered extraction events).
- **Duplicate detection** (`backend/app/services/duplicate_service.py`): a SQL
  prefilter (exact field match ∪ MySQL FULLTEXT) narrows candidates, then
  `rapidfuzz` does the real similarity scoring in Python — MySQL's FULLTEXT
  relevance scoring alone is unreliable on a small seed corpus.
- **Graceful degradation**: `GROQ_API_KEY` is optional at startup. Every
  Groq-dependent code path catches the missing-key case and returns a clean
  error (503 / SSE `error` event) instead of crashing; manual complaint entry
  never touches Groq at all.

## Project layout

```
backend/    FastAPI app, LangGraph agents, SQLAlchemy models, Alembic migrations
frontend/   React + Redux Toolkit UI (Vite)
sample_data/documents/   Sample pharma complaint documents for demoing upload
```

## Local development (without Docker)

Backend (requires MySQL reachable, e.g. via `docker compose up -d mysql`):

```bash
cd backend
python -m venv .venv && .venv/Scripts/activate  # or source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```
