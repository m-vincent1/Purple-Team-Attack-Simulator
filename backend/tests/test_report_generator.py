import json
import pytest
from pathlib import Path
from app.services.scenario_runner import run_scenario
from app.services.report_generator import generate_report
from app.core.config import settings


def test_generate_json_report(db_session, tmp_path, monkeypatch):
    import app.core.config as cfg
    monkeypatch.setattr(cfg.Settings, "generated_reports_path", property(lambda self: tmp_path))
    monkeypatch.setattr(cfg.Settings, "generated_logs_path", property(lambda self: tmp_path))

    result = run_scenario("suspicious-powershell", db_session)
    path = generate_report(result["run_id"], "json", db_session)
    assert Path(path).exists()
    with open(path) as f:
        data = json.load(f)
    assert data["run_id"] == result["run_id"]
    assert "alerts" in data
    assert data["result"]["coverage_status"] == "covered"


def test_generate_html_report(db_session, tmp_path, monkeypatch):
    import app.core.config as cfg
    monkeypatch.setattr(cfg.Settings, "generated_reports_path", property(lambda self: tmp_path))
    monkeypatch.setattr(cfg.Settings, "generated_logs_path", property(lambda self: tmp_path))

    result = run_scenario("ssh-bruteforce", db_session)
    path = generate_report(result["run_id"], "html", db_session)
    content = Path(path).read_text(encoding="utf-8")
    assert "Purple Team" in content
    assert "ssh-bruteforce" in content


def test_generate_md_report(db_session, tmp_path, monkeypatch):
    import app.core.config as cfg
    monkeypatch.setattr(cfg.Settings, "generated_reports_path", property(lambda self: tmp_path))
    monkeypatch.setattr(cfg.Settings, "generated_logs_path", property(lambda self: tmp_path))

    result = run_scenario("new-admin-user", db_session)
    path = generate_report(result["run_id"], "md", db_session)
    content = Path(path).read_text()
    assert "# Purple Team Simulation Report" in content


def test_coverage_calculation(db_session):
    from app.services.coverage_calculator import calculate_coverage
    # Before any runs
    cov = calculate_coverage(db_session)
    assert cov["total_scenarios"] == 10
    assert cov["coverage_rate"] == 0.0

    # After a run
    run_scenario("suspicious-powershell", db_session)
    cov = calculate_coverage(db_session)
    assert cov["detected_scenarios"] >= 1
    assert cov["coverage_rate"] > 0
