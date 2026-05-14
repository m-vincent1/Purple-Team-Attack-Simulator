from pydantic import BaseModel


class ReportRequest(BaseModel):
    format: str = "html"
