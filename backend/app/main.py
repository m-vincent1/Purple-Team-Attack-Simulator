from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
import app.core.database as _db_module
from app.core.database import init_db
from app.api.routes_health import router as health_router
from app.api.routes_scenarios import router as scenarios_router
from app.api.routes_runs import router as runs_router
from app.api.routes_detections import router as detections_router
from app.api.routes_reports import router as reports_router
from app.services.scenario_loader import load_all_scenarios
from app.services.scenario_loader import load_all_rules
from app.models.scenario import Scenario
from app.models.detection import DetectionRule


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    _seed_scenarios_and_rules()
    yield


def _seed_scenarios_and_rules() -> None:
    # Access SessionLocal through module so test patching is effective
    db = _db_module.SessionLocal()
    try:
        _seed_scenarios(db)
        _seed_rules(db)
    finally:
        db.close()


def _seed_scenarios(db) -> None:
    scenarios_data = load_all_scenarios()
    for data in scenarios_data:
        existing = db.get(Scenario, data["id"])
        if existing:
            continue
        mitre = data.get("mitre", {})
        scenario = Scenario(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            platform=data.get("platform", "generic"),
            tactic=mitre.get("tactic", ""),
            technique_id=mitre.get("technique_id", ""),
            technique_name=mitre.get("technique_name", ""),
            severity=data.get("severity", "medium"),
            enabled=data.get("enabled", True),
            mode=data.get("mode", "synthetic"),
            expected_detection=data.get("expected_detection"),
        )
        db.add(scenario)
    db.commit()


def _seed_rules(db) -> None:
    rules_data = load_all_rules()
    for data in rules_data:
        existing = db.get(DetectionRule, data["id"])
        if existing:
            continue
        mitre = data.get("mitre", {})
        rule = DetectionRule(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            severity=data.get("severity", "medium"),
            tactic=mitre.get("tactic", ""),
            technique_id=mitre.get("technique_id", ""),
            enabled=data.get("enabled", True),
        )
        db.add(rule)
    db.commit()


app = FastAPI(
    title="Purple Team Attack Simulator",
    description="Local defensive cybersecurity simulation platform for SOC and purple team training.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(scenarios_router)
app.include_router(runs_router)
app.include_router(detections_router)
app.include_router(reports_router)
