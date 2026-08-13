import uuid
from pathlib import Path

from app.config import get_settings

settings = get_settings()


def save_upload(filename: str, data: bytes) -> str:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    safe_suffix = Path(filename).suffix[:10]
    stored_name = f"{uuid.uuid4().hex}{safe_suffix}"
    stored_path = upload_dir / stored_name
    stored_path.write_bytes(data)
    return str(stored_path)
