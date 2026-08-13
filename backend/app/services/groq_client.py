"""Thin wrapper around Groq chat models with a JSON-mode + Pydantic-validate +
bounded-retry helper. Small/fast Groq models (e.g. llama-3.1-8b-instant) don't
reliably support native tool-calling, so structured output is obtained via
strict prompting + validation rather than function-calling.
"""

import json
import re

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, ValidationError

from app.config import get_settings
from app.core.exceptions import ExtractionFailedError, GroqNotConfiguredError

_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def get_chat_model(model_name: str, temperature: float = 0.0, streaming: bool = False) -> ChatGroq:
    settings = get_settings()
    if not settings.groq_configured:
        raise GroqNotConfiguredError(
            "GROQ_API_KEY is not configured. Add it to your .env to enable AI features."
        )
    return ChatGroq(
        model=model_name,
        api_key=settings.groq_api_key,
        temperature=temperature,
        streaming=streaming,
    )


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    match = _FENCE_RE.search(text)
    return match.group(1).strip() if match else text


def call_llm_json[T: BaseModel](
    model_name: str,
    system_prompt: str,
    user_prompt: str,
    schema_model: type[T],
    max_retries: int = 2,
    temperature: float = 0.0,
) -> T:
    llm = get_chat_model(model_name, temperature=temperature)
    messages: list = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

    last_error: Exception | None = None
    for _ in range(max_retries + 1):
        response = llm.invoke(messages)
        raw = _strip_code_fences(str(response.content))
        try:
            data = json.loads(raw)
            return schema_model.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as exc:
            last_error = exc
            messages.append(AIMessage(content=str(response.content)))
            messages.append(
                HumanMessage(
                    content=(
                        "Your previous response was not valid JSON matching the required schema. "
                        f"Error: {exc}. Respond again with ONLY valid JSON — no markdown fences, no commentary."
                    )
                )
            )

    raise ExtractionFailedError(
        f"Model {model_name} failed to produce valid structured output after {max_retries + 1} attempts: {last_error}"
    )
