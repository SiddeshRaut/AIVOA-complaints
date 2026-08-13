from datetime import datetime


def format_complaint_number(complaint_id: int, when: datetime | None = None) -> str:
    year = (when or datetime.utcnow()).year
    return f"CMP-{year}-{complaint_id:06d}"
