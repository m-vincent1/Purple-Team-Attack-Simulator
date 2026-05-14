from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)
    platform: Mapped[str] = mapped_column(String(64))
    tactic: Mapped[str] = mapped_column(String(128))
    technique_id: Mapped[str] = mapped_column(String(32))
    technique_name: Mapped[str] = mapped_column(String(256))
    severity: Mapped[str] = mapped_column(String(32))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expected_detection: Mapped[str] = mapped_column(String(128), nullable=True)
    mode: Mapped[str] = mapped_column(String(32), default="synthetic")
