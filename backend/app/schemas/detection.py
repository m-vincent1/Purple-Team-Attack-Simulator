from datetime import datetime
from pydantic import BaseModel


class AlertOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    run_id: str
    rule_id: str
    timestamp: datetime
    title: str
    severity: str
    matched_event_id: int | None
    reason: str
    mitre_technique_id: str
    mitre_tactic: str


class CoverageOut(BaseModel):
    total_scenarios: int
    total_techniques: int
    total_tactics: int
    detected_scenarios: int
    undetected_scenarios: int
    coverage_rate: float
    alerts_by_severity: dict[str, int]
    technique_coverage: list[dict]
