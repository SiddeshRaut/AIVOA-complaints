class GroqNotConfiguredError(Exception):
    """Raised when a Groq-dependent feature is used without GROQ_API_KEY set."""


class DocumentParseError(Exception):
    """Raised when an uploaded document cannot be parsed into text."""


class ExtractionFailedError(Exception):
    """Raised when the LLM extraction step cannot produce valid structured output."""
