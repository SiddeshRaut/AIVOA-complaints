"""Idempotent seed data for local/demo use. Run with:
    docker compose run --rm backend python -m scripts.seed_db

Includes two deliberate near-duplicate pairs (same product + batch number,
differently worded descriptions) so the Duplicate Complaint Detection bonus
feature has something real to catch when demoing new submissions against
this seeded history.
"""

from datetime import date

from app.database import SessionLocal
from app.models.complaint import Complaint

SEED_COMPLAINTS = [
    dict(
        complaint_number="CMP-SEED-001",
        complaint_source="Distributor",
        customer_name="MedLine Wholesale Distributors",
        product_name="Metformin HCl 500mg Tablets",
        product_strength="500mg",
        batch_number="MET-2026-0112",
        manufacturing_date=date(2025, 9, 10),
        expiry_date=date(2027, 8, 31),
        quantity_affected=120,
        quantity_unit="units",
        complaint_type="Packaging Defect",
        complaint_date=date(2026, 6, 2),
        description="Foil blister seal was broken on arrival for 4 of 20 strips in the shipment, exposing tablets to air.",
        initial_severity="Minor",
        priority="Low",
        status="Resolved",
    ),
    dict(
        complaint_number="CMP-SEED-002",
        complaint_source="Customer Portal",
        customer_name="Green Valley Pharmacy",
        product_name="Ciprofloxacin 500mg Tablets",
        product_strength="500mg",
        batch_number="CIP-2025-0987",
        manufacturing_date=date(2025, 3, 15),
        expiry_date=date(2027, 3, 14),
        quantity_affected=30,
        quantity_unit="units",
        complaint_type="Potency/Efficacy Issue",
        complaint_date=date(2026, 5, 20),
        description="Patient reported no symptomatic improvement after completing the full course; requesting quality investigation.",
        initial_severity="Major",
        priority="Medium",
        status="Under Investigation",
    ),
    dict(
        complaint_number="CMP-SEED-003",
        complaint_source="Regulatory Authority",
        customer_name="State Drug Control Office",
        product_name="Insulin Glargine Injection",
        product_strength="100 units/mL",
        batch_number="INS-2026-0034",
        manufacturing_date=date(2026, 1, 5),
        expiry_date=date(2027, 7, 4),
        quantity_affected=8,
        quantity_unit="vials",
        complaint_type="Foreign Particulate/Contamination",
        complaint_date=date(2026, 6, 15),
        description="Visible white particulate matter observed floating in two vials during routine inspection at a dispensing pharmacy.",
        initial_severity="Critical",
        priority="High",
        status="Under Investigation",
    ),
    dict(
        complaint_number="CMP-SEED-004",
        complaint_source="Sales Representative",
        customer_name="Northside Hospital Pharmacy",
        product_name="Insulin Glargine Injection",
        product_strength="100 units/mL",
        batch_number="INS-2026-0034",
        manufacturing_date=date(2026, 1, 5),
        expiry_date=date(2027, 7, 4),
        quantity_affected=3,
        quantity_unit="vials",
        complaint_type="Foreign Particulate/Contamination",
        complaint_date=date(2026, 6, 17),
        description="Pharmacist noticed small floating particles in the solution before dispensing; withheld vials from patient use.",
        initial_severity="Critical",
        priority="High",
        status="Pending Triage",
    ),
    dict(
        complaint_number="CMP-SEED-005",
        complaint_source="Email",
        customer_name="Riverside Clinic Supplies",
        product_name="Omeprazole 20mg Capsules",
        product_strength="20mg",
        batch_number="OME-2025-0765",
        manufacturing_date=date(2025, 8, 1),
        expiry_date=date(2027, 7, 31),
        quantity_affected=50,
        quantity_unit="units",
        complaint_type="Labeling Error",
        complaint_date=date(2026, 4, 11),
        description="Carton label printed as '40mg' while blister foil correctly states '20mg', creating dosing confusion risk.",
        initial_severity="Major",
        priority="High",
        status="Resolved",
    ),
    dict(
        complaint_number="CMP-SEED-006",
        complaint_source="Phone Call",
        customer_name="Individual Patient (via Pharmacovigilance)",
        product_name="Azithromycin 250mg Tablets",
        product_strength="250mg",
        batch_number="AZI-2026-0221",
        manufacturing_date=date(2025, 12, 1),
        expiry_date=date(2027, 11, 30),
        quantity_affected=1,
        quantity_unit="units",
        complaint_type="Adverse Event",
        complaint_date=date(2026, 7, 3),
        description="Patient reported severe nausea and abdominal cramping within an hour of the first dose; sought medical attention.",
        initial_severity="Major",
        priority="High",
        status="Under Investigation",
    ),
    dict(
        complaint_number="CMP-SEED-007",
        complaint_source="Distributor",
        customer_name="MedLine Wholesale Distributors",
        product_name="Paracetamol 650mg Tablets",
        product_strength="650mg",
        batch_number="PCM-2026-0450",
        manufacturing_date=date(2026, 2, 20),
        expiry_date=date(2028, 2, 19),
        quantity_affected=200,
        quantity_unit="units",
        complaint_type="Physical/Appearance Defect",
        complaint_date=date(2026, 7, 10),
        description="Approximately 10% of tablets in the received cartons were chipped or cracked at the edges.",
        initial_severity="Minor",
        priority="Medium",
        status="Pending Triage",
    ),
    dict(
        complaint_number="CMP-SEED-008",
        complaint_source="Customer Portal",
        customer_name="Fairview Retail Pharmacy",
        product_name="Paracetamol 650mg Tablets",
        product_strength="650mg",
        batch_number="PCM-2026-0450",
        manufacturing_date=date(2026, 2, 20),
        expiry_date=date(2028, 2, 19),
        quantity_affected=45,
        quantity_unit="units",
        complaint_type="Physical/Appearance Defect",
        complaint_date=date(2026, 7, 12),
        description="Pharmacist flagged cracked and chipped tablets in several bottles from this batch during shelf restocking.",
        initial_severity="Minor",
        priority="Medium",
        status="Pending Triage",
    ),
    dict(
        complaint_number="CMP-SEED-009",
        complaint_source="Customer Portal",
        customer_name="Green Valley Pharmacy",
        product_name="Ciprofloxacin 500mg Tablets",
        product_strength="500mg",
        batch_number="CIP-2026-0110",
        manufacturing_date=date(2026, 1, 18),
        expiry_date=date(2028, 1, 17),
        quantity_affected=20,
        quantity_unit="units",
        complaint_type="Delayed Onset of Action",
        complaint_date=date(2026, 7, 25),
        description="Prescriber reported slower-than-expected symptomatic relief compared to prior batches of the same product.",
        initial_severity="Minor",
        priority="Low",
        status="Pending Triage",
    ),
    dict(
        complaint_number="CMP-SEED-010",
        complaint_source="Regulatory Authority",
        customer_name="State Drug Control Office",
        product_name="Metformin HCl 500mg Tablets",
        product_strength="500mg",
        batch_number="MET-2026-0298",
        manufacturing_date=date(2026, 3, 1),
        expiry_date=date(2028, 2, 29),
        quantity_affected=500,
        quantity_unit="units",
        complaint_type="Counterfeit Suspicion",
        complaint_date=date(2026, 8, 1),
        description="Field inspection found packaging with inconsistent holographic seal and print quality versus authenticated stock.",
        initial_severity="Critical",
        priority="High",
        status="Under Investigation",
    ),
]


def seed() -> None:
    db = SessionLocal()
    try:
        existing = {
            c.complaint_number
            for c in db.query(Complaint.complaint_number)
            .filter(Complaint.complaint_number.like("CMP-SEED-%"))
            .all()
        }

        inserted = 0
        for row in SEED_COMPLAINTS:
            if row["complaint_number"] in existing:
                continue
            db.add(Complaint(**row))
            inserted += 1

        db.commit()
        print(f"Seed complete: inserted {inserted} new complaint(s), {len(existing)} already present.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
