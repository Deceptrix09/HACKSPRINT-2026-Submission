"""Main entry point for Part B:  triage_incident(text, attachments) -> TriageResult"""
import time
from dataclasses import dataclass, field

from google import genai
from google.genai import types

from . import config
from .postprocess import apply_rules
from .schema import Incident


@dataclass
class Attachment:
    name: str
    data: bytes
    mime: str  # image/jpeg, image/png, application/pdf


@dataclass
class TriageResult:
    incident: Incident
    review_reasons: list[str]
    audit: dict = field(default_factory=dict)


_client = None


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(
            vertexai=True, project=config.GCP_PROJECT, location=config.GCP_LOCATION
        )
    return _client


def triage_incident(text: str | None, attachments: list[Attachment] | None = None,
                    retries: int = 3) -> TriageResult:
    attachments = attachments or []
    instructions = config.PROMPT_PATH.read_text(encoding="utf-8")
    sop = config.SOP_PATH.read_text(encoding="utf-8")

    parts: list = []
    for a in attachments:
        parts.append(f"Attached file: {a.name}")
        parts.append(types.Part.from_bytes(data=a.data, mime_type=a.mime))
    parts.append(f"Text report:\n{text}" if text else "No text report was provided.")
    parts.append(f"SOP RULES:\n{sop}")

    last_error = None
    for attempt in range(retries):
        try:
            resp = _get_client().models.generate_content(
                model=config.GEMINI_MODEL,
                contents=parts,
                config=types.GenerateContentConfig(
                    system_instruction=instructions,
                    response_mime_type="application/json",
                    response_schema=Incident,
                    temperature=0.2,
                ),
            )
            incident = resp.parsed
            if incident is None:
                incident = Incident.model_validate_json(resp.text)
            incident, reasons = apply_rules(incident)
            audit = {
                "model": config.GEMINI_MODEL,
                "input_text": text,
                "input_files": [a.name for a in attachments],
                "prompt": instructions,
                "raw_response": resp.text,
                "review_reasons": reasons,
            }
            return TriageResult(incident, reasons, audit)
        except Exception as e:  # retry on any failure
            last_error = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Triage failed after {retries} attempts: {last_error}")
