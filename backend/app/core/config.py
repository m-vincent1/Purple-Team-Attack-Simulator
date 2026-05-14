from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./purple_team.db"
    LOG_LEVEL: str = "INFO"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    SCENARIOS_DIR: str = "scenarios"
    RULES_DIR: str = "rules"
    GENERATED_LOGS_DIR: str = "../generated_logs"
    GENERATED_REPORTS_DIR: str = "../generated_reports"
    LAB_SANDBOX_DIR: str = "../lab_sandbox"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    @property
    def scenarios_path(self) -> Path:
        return Path(__file__).parent.parent.parent / self.SCENARIOS_DIR

    @property
    def rules_path(self) -> Path:
        return Path(__file__).parent.parent.parent / self.RULES_DIR

    @property
    def generated_logs_path(self) -> Path:
        p = Path(__file__).parent.parent.parent / self.GENERATED_LOGS_DIR
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def generated_reports_path(self) -> Path:
        p = Path(__file__).parent.parent.parent / self.GENERATED_REPORTS_DIR
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def lab_sandbox_path(self) -> Path:
        p = Path(__file__).parent.parent.parent / self.LAB_SANDBOX_DIR
        p.mkdir(parents=True, exist_ok=True)
        return p


settings = Settings()
