"""Blocks until MySQL accepts connections. Run before Alembic on container start.

MySQL's Docker healthcheck can report healthy a moment before it actually accepts
new connections under load, so the app layer retries independently rather than
trusting depends_on/healthcheck alone.
"""

import sys

from sqlalchemy import create_engine, text
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings


@retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=1, max=15))
def wait_for_db() -> None:
    settings = get_settings()
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    engine.dispose()


if __name__ == "__main__":
    try:
        wait_for_db()
        print("Database is ready.")
    except Exception as exc:  # noqa: BLE001
        print(f"Database never became ready: {exc}", file=sys.stderr)
        sys.exit(1)
