from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services import duplicate_service


def _fake_complaint(**overrides):
    defaults = dict(
        id=1,
        complaint_number="CMP-2026-000001",
        product_name="Metformin HCl 500mg Tablets",
        batch_number="MET-2026-0112",
        complaint_type="Packaging Defect",
        description="Foil seal broken on several strips.",
        customer_name="Test Customer",
        created_at=datetime(2026, 1, 1),
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_find_duplicates_scores_exact_match_highest(monkeypatch):
    candidate = _fake_complaint()
    monkeypatch.setattr(duplicate_service, "_prefilter", lambda *a, **k: [candidate])

    results = duplicate_service.find_duplicates(
        db=MagicMock(),
        product_name="Metformin HCl 500mg Tablets",
        batch_number="MET-2026-0112",
        complaint_type="Packaging Defect",
        description="Foil seal broken on several strips.",
    )

    assert len(results) == 1
    assert results[0]["complaint_id"] == 1
    assert results[0]["similarity_score"] == 100.0
    assert set(results[0]["matched_fields"]) == {
        "product_name",
        "batch_number",
        "complaint_type",
        "description",
    }


def test_find_duplicates_filters_below_threshold(monkeypatch):
    candidate = _fake_complaint(
        product_name="Completely Different Product",
        batch_number="XYZ-0000",
        complaint_type="Labeling Error",
        description="Totally unrelated issue about carton printing quality.",
    )
    monkeypatch.setattr(duplicate_service, "_prefilter", lambda *a, **k: [candidate])

    results = duplicate_service.find_duplicates(
        db=MagicMock(),
        product_name="Metformin HCl 500mg Tablets",
        batch_number="MET-2026-0112",
        complaint_type="Packaging Defect",
        description="Foil seal broken on several strips.",
    )

    assert results == []


def test_find_duplicates_returns_top_five(monkeypatch):
    candidates = [_fake_complaint(id=i, complaint_number=f"CMP-{i}") for i in range(1, 9)]
    monkeypatch.setattr(duplicate_service, "_prefilter", lambda *a, **k: candidates)

    results = duplicate_service.find_duplicates(
        db=MagicMock(),
        product_name="Metformin HCl 500mg Tablets",
        batch_number="MET-2026-0112",
        complaint_type="Packaging Defect",
        description="Foil seal broken on several strips.",
    )

    assert len(results) == duplicate_service.MAX_CANDIDATES
