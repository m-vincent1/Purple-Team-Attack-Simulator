import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alert import Alert
from app.models.log_event import LogEvent
from app.models.run import SimulationRun
from app.models.scenario import Scenario
from app.schemas.detection import AlertOut
from app.schemas.log_event import LogEventOut
from app.schemas.run import RunOut, ValidationResult
from app.services.scenario_runner import run_scenario

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("/run-all")
def run_all_scenarios(db: Session = Depends(get_db)):
    scenarios = db.query(Scenario).filter(Scenario.enabled == True).all()  # noqa: E712
    results = []
    for scenario in scenarios:
        try:
            result = run_scenario(scenario.id, db)
            results.append(result)
        except Exception as e:
            results.append({"scenario_id": scenario.id, "error": str(e)})
    return {"results": results, "total": len(results)}


@router.get("", response_model=list[RunOut])
def list_runs(db: Session = Depends(get_db)):
    return db.query(SimulationRun).order_by(SimulationRun.started_at.desc()).all()


@router.get("/{run_id}", response_model=RunOut)
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.get(SimulationRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/{run_id}/logs", response_model=list[LogEventOut])
def get_run_logs(run_id: str, db: Session = Depends(get_db)):
    return db.query(LogEvent).filter(LogEvent.run_id == run_id).all()


@router.get("/{run_id}/alerts", response_model=list[AlertOut])
def get_run_alerts(run_id: str, db: Session = Depends(get_db)):
    return db.query(Alert).filter(Alert.run_id == run_id).all()


@router.post("/{run_id}/validate", response_model=ValidationResult)
def validate_run(run_id: str, db: Session = Depends(get_db)):
    run = db.get(SimulationRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    scenario = db.get(Scenario, run.scenario_id)
    alerts = db.query(Alert).filter(Alert.run_id == run_id).all()
    detected_rule_ids = {a.rule_id for a in alerts}
    expected = scenario.expected_detection if scenario else None
    detected = (expected in detected_rule_ids) if expected else len(detected_rule_ids) > 0
    return ValidationResult(
        run_id=run_id,
        scenario_id=run.scenario_id,
        expected_detection=expected,
        detected=detected,
        alerts_count=len(alerts),
        coverage_status="covered" if detected else "not_detected",
    )
