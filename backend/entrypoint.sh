#!/usr/bin/env bash
set -e

echo "Waiting for database and applying migrations..."
python -m app.core.wait_for_db
alembic upgrade head

if [ "$#" -gt 0 ]; then
  echo "Running: $*"
  exec "$@"
fi

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
