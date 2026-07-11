"""
PII Detection and Redaction Pipeline
=====================================
Uses Microsoft Presidio to detect and redact PII from user inputs
before they reach a language model or are written to audit logs.

Install:
    pip install presidio-analyzer presidio-anonymizer
    python -m spacy download en_core_web_lg  # Presidio's default NER model

Usage:
    from pii_redaction import redact_input, PIIRedactionResult

    result = redact_input("My name is Jane Smith and my email is jane@example.com")
    print(result.redacted_text)   # "My name is <PERSON> and my email is <EMAIL_ADDRESS>"
    print(result.entity_count)    # 2
    print(result.has_pii)         # True
"""

from dataclasses import dataclass, field
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Entity types to detect. Extend for domain-specific identifiers.
# ---------------------------------------------------------------------------
DEFAULT_ENTITY_TYPES = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "CREDIT_CARD",
    "US_SSN",
    "US_BANK_NUMBER",
    "IBAN_CODE",
    "MEDICAL_LICENSE",
    "IP_ADDRESS",
    "US_PASSPORT",
    "US_DRIVER_LICENSE",
    "LOCATION",           # Addresses
    "DATE_TIME",          # Birthdates — context-dependent; enable if needed
    "NRP",                # Nationalities, religions, political groups
    "URL",                # URLs may contain user-identifying paths
]


@dataclass
class PIIRedactionResult:
    """Result of a PII redaction pass on a single text input."""
    original_length: int
    redacted_text: str
    entity_count: int
    entity_types_found: list[str] = field(default_factory=list)
    has_pii: bool = False
    error: Optional[str] = None


def build_engines():
    """
    Initialize Presidio analyzer and anonymizer.
    Called once at module import; cached for reuse.
    Heavy to initialize — do not call per-request.
    """
    try:
        from presidio_analyzer import AnalyzerEngine
        from presidio_anonymizer import AnonymizerEngine
        analyzer = AnalyzerEngine()
        anonymizer = AnonymizerEngine()
        return analyzer, anonymizer
    except ImportError as e:
        raise ImportError(
            "presidio-analyzer and presidio-anonymizer are required. "
            "Run: pip install presidio-analyzer presidio-anonymizer "
            "and: python -m spacy download en_core_web_lg"
        ) from e


# Module-level singletons — initialize once
_analyzer = None
_anonymizer = None


def _get_engines():
    global _analyzer, _anonymizer
    if _analyzer is None:
        _analyzer, _anonymizer = build_engines()
    return _analyzer, _anonymizer


def redact_input(
    text: str,
    language: str = "en",
    entity_types: list[str] = None,
    score_threshold: float = 0.5,
) -> PIIRedactionResult:
    """
    Detect and redact PII from a text string.

    Args:
        text: The raw user input to scan.
        language: ISO 639-1 language code. Presidio supports en, de, es, fr, and others.
        entity_types: List of PII entity types to detect. Defaults to DEFAULT_ENTITY_TYPES.
        score_threshold: Minimum confidence score to consider a detection. 0.5 is a
                         reasonable default; lower values increase recall at the cost
                         of false positives.

    Returns:
        PIIRedactionResult with the redacted text and detection metadata.
        The original text is never stored or returned.
    """
    if not text or not text.strip():
        return PIIRedactionResult(
            original_length=len(text),
            redacted_text=text,
            entity_count=0,
            has_pii=False,
        )

    if entity_types is None:
        entity_types = DEFAULT_ENTITY_TYPES

    try:
        analyzer, anonymizer = _get_engines()

        # Analyze: find all PII entities
        analysis_results = analyzer.analyze(
            text=text,
            language=language,
            entities=entity_types,
            score_threshold=score_threshold,
        )

        if not analysis_results:
            return PIIRedactionResult(
                original_length=len(text),
                redacted_text=text,
                entity_count=0,
                has_pii=False,
            )

        # Anonymize: replace detected entities with placeholders
        # e.g., "Jane Smith" → "<PERSON>", "jane@acme.com" → "<EMAIL_ADDRESS>"
        anonymized = anonymizer.anonymize(
            text=text,
            analyzer_results=analysis_results,
        )

        entity_types_found = list({r.entity_type for r in analysis_results})

        logger.info(
            "PII redaction applied",
            extra={
                "entity_count": len(analysis_results),
                "entity_types": entity_types_found,
                # Log metadata only — never log the original text
            },
        )

        return PIIRedactionResult(
            original_length=len(text),
            redacted_text=anonymized.text,
            entity_count=len(analysis_results),
            entity_types_found=entity_types_found,
            has_pii=True,
        )

    except Exception as e:
        logger.error("PII redaction failed: %s", str(e))
        # Fail closed: if redaction fails, do not pass the original text to the model.
        return PIIRedactionResult(
            original_length=len(text),
            redacted_text="[INPUT REDACTED — PII SCAN ERROR]",
            entity_count=0,
            has_pii=True,  # Treat as PII to be safe
            error=str(e),
        )


def should_refuse_input(result: PIIRedactionResult, refuse_on_pii: bool = False) -> bool:
    """
    Decide whether to refuse the request based on PII detection results.

    Two strategies:
    - refuse_on_pii=False (default): redact and continue. The user doesn't know
      their PII was found; it's silently scrubbed before the model sees it.
    - refuse_on_pii=True: refuse the request and tell the user. Appropriate when
      the presence of PII suggests the user is trying to submit sensitive data
      that the feature should not process (e.g., uploading health records to a
      general-purpose assistant).
    """
    if not result.has_pii:
        return False
    return refuse_on_pii


# ---------------------------------------------------------------------------
# Example usage and test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_inputs = [
        "My name is Jane Smith and I live at 123 Main St, Boston MA.",
        "Call me at 617-555-0147 or email jane.smith@example.com",
        "My SSN is 123-45-6789 and my credit card is 4111 1111 1111 1111",
        "This input contains no personal information at all.",
        "Patient ID: MED-2024-00192, DOB: 1985-03-15",
    ]

    print("PII Redaction Test\n" + "=" * 50)
    for text in test_inputs:
        result = redact_input(text)
        print(f"\nOriginal length : {result.original_length} chars")
        print(f"Has PII         : {result.has_pii}")
        print(f"Entities found  : {result.entity_count} ({', '.join(result.entity_types_found)})")
        print(f"Redacted text   : {result.redacted_text}")
