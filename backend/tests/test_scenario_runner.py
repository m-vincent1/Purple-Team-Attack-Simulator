import pytest
from app.services.scenario_runner import run_scenario
from app.models.run import SimulationRun
from app.models.log_event import LogEvent
from app.models.alert import Alert


def test_run_suspicious_powershell(db_session):
    result = run_scenario("suspicious-powershell", db_session)
    assert result["run_id"]
    assert result["events_generated"] > 0
    assert result["coverage_status"] == "covered"
    assert result["alerts_count"] > 0


def test_run_creates_db_records(db_session):
    result = run_scenario("ssh-bruteforce", db_session)
    run_id = result["run_id"]
    run = db_session.get(SimulationRun, run_id)
    assert run is not None
    assert run.status == "completed"
    logs = db_session.query(LogEvent).filter(LogEvent.run_id == run_id).all()
    assert len(logs) > 0
    alerts = db_session.query(Alert).filter(Alert.run_id == run_id).all()
    assert len(alerts) > 0


def test_run_writes_jsonl(db_session, tmp_path, monkeypatch):
    from app.core import config
    monkeypatch.setattr(config.settings, "GENERATED_LOGS_DIR", str(tmp_path))

    # Patch the path property
    import app.core.config as cfg
    original = cfg.Settings.generated_logs_path.fget
    monkeypatch.setattr(
        cfg.Settings, "generated_logs_path",
        property(lambda self: tmp_path),
        raising=True,
    )
    result = run_scenario("new-admin-user", db_session)
    log_file = tmp_path / f"{result['run_id']}.jsonl"
    assert log_file.exists()
    lines = log_file.read_text().strip().split("\n")
    assert len(lines) > 0


def test_invalid_scenario_raises(db_session):
    with pytest.raises(ValueError):
        run_scenario("nonexistent-scenario", db_session)
