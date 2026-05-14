"""Calculates MITRE ATT&CK detection coverage across all simulation runs."""

import json
from typing import Any

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.run import SimulationRun
from app.models.scenario import Scenario


def calculate_coverage(db: Session) -> dict[str, Any]:
    scenarios = db.query(Scenario).filter(Scenario.enabled == True).all()  # noqa: E712
    runs = db.query(SimulationRun).filter(SimulationRun.status == "completed").all()
    alerts = db.query(Alert).all()

    total_scenarios = len(scenarios)
    techniques = {s.technique_id for s in scenarios}
    tactics = {s.tactic for s in scenarios}

    run_ids_with_alerts = {a.run_id for a in alerts}
    scenario_ids_with_runs: dict[str, list[str]] = {}
    for run in runs:
        scenario_ids_with_runs.setdefault(run.scenario_id, []).append(run.id)

    detected_scenarios = 0
    undetected_scenarios = 0
    for scenario in scenarios:
        run_ids = scenario_ids_with_runs.get(scenario.id, [])
        if not run_ids:
            continue
        if any(rid in run_ids_with_alerts for rid in run_ids):
            detected_scenarios += 1
        else:
            undetected_scenarios += 1

    tested_scenarios = detected_scenarios + undetected_scenarios
    coverage_rate = (detected_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0.0

    alerts_by_severity: dict[str, int] = {}
    for alert in alerts:
        alerts_by_severity[alert.severity] = alerts_by_severity.get(alert.severity, 0) + 1

    technique_coverage = []
    for scenario in scenarios:
        run_ids = scenario_ids_with_runs.get(scenario.id, [])
        if not run_ids:
            status = "not_tested"
        elif any(rid in run_ids_with_alerts for rid in run_ids):
            status = "covered"
        else:
            status = "not_detected"
        technique_coverage.append({
            "scenario_id": scenario.id,
            "technique_id": scenario.technique_id,
            "technique_name": scenario.technique_name,
            "tactic": scenario.tactic,
            "status": status,
        })

    return {
        "total_scenarios": total_scenarios,
        "total_techniques": len(techniques),
        "total_tactics": len(tactics),
        "detected_scenarios": detected_scenarios,
        "undetected_scenarios": undetected_scenarios,
        "coverage_rate": round(coverage_rate, 1),
        "alerts_by_severity": alerts_by_severity,
        "technique_coverage": technique_coverage,
    }
