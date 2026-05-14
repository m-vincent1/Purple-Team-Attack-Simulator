from datetime import datetime
from pydantic import BaseModel


class RunOut(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    scenario_id: str
    status: str
    started_at: datetime
    finished_at: datetime | None
    mode: str
    result_summary: str | None


class ValidationResult(BaseModel):
    run_id: str
    scenario_id: str
    expected_detection: str | None
    detected: bool
    alerts_count: int
    coverage_status: str
