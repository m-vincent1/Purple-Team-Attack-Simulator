"""Orchestrates a full simulation run: generate logs → detect → persist → write JSONL."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.alert import Alert
from app.models.log_event import LogEvent
from app.models.run import SimulationRun
from app.models.scenario import Scenario
from app.services.detection_engine import run_detection
from app.services.scenario_loader import load_all_rules
from app.services.synthetic_log_generator import generate_events_for_scenario


def _build_run_id(scenario_id: str) -> str:
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return f"{ts}-{scenario_id}"


def run_scenario(scenario_id: str, db: Session) -> dict[str, Any]:
    scenario = db.get(Scenario, scenario_id)
    if scenario is None:
        raise ValueError(f"Scenario not found: {scenario_id}")

    run_id = _build_run_id(scenario_id)
    run = SimulationRun(
        id=run_id,
        scenario_id=scenario_id,
        status="running",
        started_at=datetime.utcnow(),
        mode="synthetic",
    )
    db.add(run)
    db.commit()

    try:
        base_time = datetime.utcnow()
        raw_events = generate_events_for_scenario(scenario_id, base_time)

        log_event_objects = []
        for evt in raw_events:
            ts_str = evt.get("timestamp", base_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
            try:
                ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                ts = base_time
            le = LogEvent(
                run_id=run_id,
                timestamp=ts,
                source=evt.get("source", ""),
                host=evt.get("host", ""),
                user=evt.get("user", ""),
                event_type=evt.get("event_type", ""),
                event_id=evt.get("event_id"),
                process_name=evt.get("process_name"),
                command_line=evt.get("command_line"),
                src_ip=evt.get("src_ip"),
                dst_ip=evt.get("dst_ip"),
                raw_message=evt.get("raw_message"),
                event_json=json.dumps(evt),
            )
            db.add(le)
            log_event_objects.append(le)
        db.commit()
        db.refresh(log_event_objects[0])  # get IDs assigned

        # Reload to get IDs
        db.expire_all()
        persisted_events = (
            db.query(LogEvent).filter(LogEvent.run_id == run_id).all()
        )

        rules = load_all_rules()
        alerts_data = run_detection(raw_events, rules)

        alert_objects = []
        for a in alerts_data:
            idx = a["event_index"]
            matched_id = persisted_events[idx].id if idx < len(persisted_events) else None
            alert_obj = Alert(
                run_id=run_id,
                rule_id=a["rule_id"],
                title=a["rule_name"],
                severity=a["severity"],
                matched_event_id=matched_id,
                reason=a["reason"],
                mitre_technique_id=a["mitre_technique_id"],
                mitre_tactic=a["mitre_tactic"],
            )
            db.add(alert_obj)
            alert_objects.append(alert_obj)
        db.commit()

        # Write JSONL
        _write_jsonl(run_id, raw_events)

        detected_rule_ids = {a["rule_id"] for a in alerts_data}
        expected = scenario.expected_detection
        detected = expected in detected_rule_ids if expected else len(detected_rule_ids) > 0
        coverage_status = "covered" if detected else "not_detected"

        summary = {
            "events_generated": len(raw_events),
            "alerts_count": len(alert_objects),
            "detected": detected,
            "coverage_status": coverage_status,
            "rules_triggered": list(detected_rule_ids),
        }

        run.status = "completed"
        run.finished_at = datetime.utcnow()
        run.result_summary = json.dumps(summary)
        db.commit()

        return {
            "run_id": run_id,
            "scenario_id": scenario_id,
            "events_generated": len(raw_events),
            "alerts_count": len(alert_objects),
            "detected": detected,
            "coverage_status": coverage_status,
            "log_file": str(settings.generated_logs_path / f"{run_id}.jsonl"),
        }

    except Exception as exc:
        run.status = "failed"
        run.finished_at = datetime.utcnow()
        run.result_summary = json.dumps({"error": str(exc)})
        db.commit()
        raise


def _write_jsonl(run_id: str, events: list[dict]) -> Path:
    log_file = settings.generated_logs_path / f"{run_id}.jsonl"
    with open(log_file, "w", encoding="utf-8") as f:
        for evt in events:
            f.write(json.dumps(evt) + "\n")
    return log_file
