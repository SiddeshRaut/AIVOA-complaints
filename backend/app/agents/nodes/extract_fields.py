from app.agents.prompts.extraction_prompt import EXTRACTION_SYSTEM_PROMPT, build_extraction_user_prompt
from app.agents.state import ExtractionState
from app.config import get_settings
from app.core.exceptions import ExtractionFailedError, GroqNotConfiguredError
from app.schemas.extraction import ExtractedComplaintFields
from app.services.groq_client import call_llm_json


def extract_fields(state: ExtractionState) -> dict:
    settings = get_settings()
    warnings = list(state.get("warnings", []))

    try:
        result = call_llm_json(
            model_name=settings.groq_extraction_model,
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
            user_prompt=build_extraction_user_prompt(state.get("document_text", "")),
            schema_model=ExtractedComplaintFields,
        )
        fields = {name: field.model_dump() for name, field in result}
    except (GroqNotConfiguredError, ExtractionFailedError) as exc:
        warnings.append(str(exc))
        fields = {
            name: {"value": None, "confidence": 0.0}
            for name in ExtractedComplaintFields.model_fields
        }

    return {"extracted_fields": fields, "warnings": warnings}
