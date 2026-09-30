"""Plain-Python safety rules. They only ever escalate to human review."""
from .config import CONFIDENCE_THRESHOLD, CRITICAL_MIN_CONFIDENCE
from .schema import Incident


def apply_rules(incident: Incident) -> tuple[Incident, list[str]]:
    reasons: list[str] = []
    incident.confidence = max(0.0, min(1.0, incident.confidence))

    if incident.confidence < CONFIDENCE_THRESHOLD:
        reasons.append(f"Low confidence ({incident.confidence:.2f})")
    if incident.conflicts:
        reasons.append("Conflicting information between sources")
    if incident.severity == "Critical" and incident.confidence < CRITICAL_MIN_CONFIDENCE:
        reasons.append("Critical severity with confidence below 0.8")
    if not incident.evidence:
        reasons.append("No evidence cited")
    if incident.location.text.strip().lower() in ("", "unknown", "unspecified", "n/a"):
        reasons.append("Location unknown")
    if not incident.recommended_actions:
        reasons.append("No recommended actions")

    if reasons:
        incident.needs_human_review = True
    return incident, reasons
