"""The incident contract shared with Part B (database) and Part C (dashboard)."""
from typing import Literal
from pydantic import BaseModel

IncidentType = Literal[
    "flood", "fire", "building_collapse", "earthquake",
    "landslide", "medical", "road_accident", "other",
]


class Location(BaseModel):
    text: str
    lat: float | None = None
    lng: float | None = None


class Evidence(BaseModel):
    source: str
    finding: str


class Incident(BaseModel):
    type: IncidentType
    location: Location
    severity: Literal["Critical", "High", "Medium", "Low"]
    people_at_risk: int | None = None
    recommended_actions: list[str]
    confidence: float
    needs_human_review: bool
    evidence: list[Evidence]
    conflicts: list[str]
    reasoning: str
    sop_references: list[str]
