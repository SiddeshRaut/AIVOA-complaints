"""Bonus feature: AI Risk Classification — suggests Initial Severity and Priority."""

from app.agents.prompts.risk_prompt import RISK_SYSTEM_PROMPT, build_risk_user_prompt
from app.agents.state import ExtractionState
from app.config import get_settings
from app.core.exceptions import ExtractionFailedError, GroqNotConfiguredError
from app.schemas.extraction import RiskClassification
from app.services.groq_client import call_llm_json


def risk_classification(state: ExtractionState) -> dict:
    settings = get_settings()
    warnings = list(state.get("warnings", []))
    fields = state.get("extracted_fields", {})

    product_name = (fields.get("product_name") or {}).get("value") or ""
    complaint_type = (fields.get("complaint_type") or {}).get("value") or ""
    description = (fields.get("description") or {}).get("value") or ""

    if not description:
        return {"risk_severity": None, "risk_priority": None, "risk_rationale": None}

    try:
        result = call_llm_json(
            model_name=settings.groq_chat_model,
            system_prompt=RISK_SYSTEM_PROMPT,
            user_prompt=build_risk_user_prompt(product_name, complaint_type, description),
            schema_model=RiskClassification,
        )
        return {
            "risk_severity": result.severity,
            "risk_priority": result.priority,
            "risk_rationale": result.rationale,
        }
    except (GroqNotConfiguredError, ExtractionFailedError) as exc:
        warnings.append(str(exc))
        return {
            "risk_severity": None,
            "risk_priority": None,
            "risk_rationale": None,
            "warnings": warnings,
        }
