"""Generates HTML, Markdown and JSON reports from simulation run data."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.alert import Alert
from app.models.log_event import LogEvent
from app.models.run import SimulationRun
from app.models.scenario import Scenario


def _get_templates_dir() -> Path:
    return Path(__file__).parent.parent.parent / "reports" / "templates"


def _collect_report_data(run_id: str, db: Session) -> dict[str, Any]:
    run = db.get(SimulationRun, run_id)
    if run is None:
        raise ValueError(f"Run not found: {run_id}")
    scenario = db.get(Scenario, run.scenario_id)
    logs = db.query(LogEvent).filter(LogEvent.run_id == run_id).order_by(LogEvent.timestamp).all()
    alerts = db.query(Alert).filter(Alert.run_id == run_id).all()

    summary = json.loads(run.result_summary) if run.result_summary else {}

    return {
        "run": run,
        "scenario": scenario,
        "logs": logs,
        "alerts": alerts,
        "summary": summary,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_logs": len(logs),
        "total_alerts": len(alerts),
        "coverage_status": summary.get("coverage_status", "unknown"),
    }


def generate_report(run_id: str, fmt: str, db: Session) -> str:
    """Generate a report in the given format. Returns the file path."""
    data = _collect_report_data(run_id, db)

    if fmt == "json":
        return _generate_json_report(run_id, data)
    elif fmt == "md":
        return _generate_md_report(run_id, data)
    else:
        return _generate_html_report(run_id, data)


def _generate_json_report(run_id: str, data: dict) -> str:
    run = data["run"]
    scenario = data["scenario"]
    payload = {
        "report_type": "purple_team_simulation",
        "generated_at": data["generated_at"],
        "run_id": run_id,
        "scenario": {
            "id": scenario.id if scenario else None,
            "name": scenario.name if scenario else None,
            "platform": scenario.platform if scenario else None,
            "tactic": scenario.tactic if scenario else None,
            "technique_id": scenario.technique_id if scenario else None,
            "severity": scenario.severity if scenario else None,
        },
        "result": {
            "status": run.status,
            "started_at": run.started_at.isoformat(),
            "finished_at": run.finished_at.isoformat() if run.finished_at else None,
            "total_logs": data["total_logs"],
            "total_alerts": data["total_alerts"],
            "coverage_status": data["coverage_status"],
        },
        "alerts": [
            {
                "rule_id": a.rule_id,
                "title": a.title,
                "severity": a.severity,
                "reason": a.reason,
                "mitre_technique_id": a.mitre_technique_id,
                "mitre_tactic": a.mitre_tactic,
            }
            for a in data["alerts"]
        ],
    }
    out_path = settings.generated_reports_path / f"{run_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)
    return str(out_path)


def _generate_md_report(run_id: str, data: dict) -> str:
    env = _get_jinja_env()
    tmpl = env.get_template("report.md.j2")
    content = tmpl.render(**data)
    out_path = settings.generated_reports_path / f"{run_id}.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return str(out_path)


def _generate_html_report(run_id: str, data: dict) -> str:
    env = _get_jinja_env()
    tmpl = env.get_template("report.html.j2")
    content = tmpl.render(**data)
    out_path = settings.generated_reports_path / f"{run_id}.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return str(out_path)


def _get_jinja_env() -> Environment:
    templates_dir = _get_templates_dir()
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html"]),
    )
