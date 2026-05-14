from datetime import datetime
from pydantic import BaseModel


class ScenarioOut(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    name: str
    description: str
    platform: str
    tactic: str
    technique_id: str
    technique_name: str
    severity: str
    enabled: bool
    mode: str
    expected_detection: str | None
    created_at: datetime
