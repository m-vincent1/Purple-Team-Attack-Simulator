from datetime import datetime
from pydantic import BaseModel


class LogEventOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    run_id: str
    timestamp: datetime
    source: str
    host: str
    user: str
    event_type: str
    event_id: int | None
    process_name: str | None
    command_line: str | None
    src_ip: str | None
    dst_ip: str | None
    raw_message: str | None
