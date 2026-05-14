import pytest
from datetime import datetime
from app.services.detection_engine import run_detection, _event_matches_rule
from app.services.synthetic_log_generator import generate_events_for_scenario
from app.services.scenario_loader import load_all_rules, load_all_scenarios


def test_powershell_detection():
    events = generate_events_for_scenario("suspicious-powershell")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "suspicious_powershell_rule" in rule_ids


def test_ssh_bruteforce_detection():
    events = generate_events_for_scenario("ssh-bruteforce")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "ssh_bruteforce_rule" in rule_ids


def test_new_admin_user_detection():
    events = generate_events_for_scenario("new-admin-user")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "new_admin_user_rule" in rule_ids


def test_scheduled_task_detection():
    events = generate_events_for_scenario("scheduled-task-creation")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "scheduled_task_rule" in rule_ids


def test_temp_process_detection():
    events = generate_events_for_scenario("temp-process-execution")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "temp_process_rule" in rule_ids


def test_curl_download_detection():
    events = generate_events_for_scenario("suspicious-curl-download")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "suspicious_curl_rule" in rule_ids


def test_process_masquerading_detection():
    events = generate_events_for_scenario("process-masquerading")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "process_masquerading_rule" in rule_ids


def test_abnormal_login_detection():
    events = generate_events_for_scenario("abnormal-login-time")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "abnormal_login_time_rule" in rule_ids


def test_webshell_detection():
    events = generate_events_for_scenario("webshell-like-request")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "webshell_like_request_rule" in rule_ids


def test_dns_exfil_detection():
    events = generate_events_for_scenario("dns-exfil-pattern")
    rules = load_all_rules()
    alerts = run_detection(events, rules)
    rule_ids = {a["rule_id"] for a in alerts}
    assert "dns_exfil_pattern_rule" in rule_ids


def test_benign_event_no_alert():
    benign = [{
        "timestamp": "2026-01-01T10:00:00Z",
        "source": "windows_security",
        "host": "WIN-LAB-01",
        "user": "analyst",
        "event_type": "process_creation",
        "event_id": 4688,
        "process_name": "notepad.exe",
        "command_line": "notepad.exe C:\\Users\\analyst\\notes.txt",
        "src_ip": None,
        "dst_ip": None,
        "raw_message": "Benign notepad launch",
    }]
    rules = load_all_rules()
    alerts = run_detection(benign, rules)
    assert len(alerts) == 0


def test_contains_matcher():
    rule = {
        "id": "test_rule", "name": "Test", "severity": "low",
        "detection": {
            "condition": "any",
            "fields": {"command_line": {"contains": ["-enc"]}},
        },
    }
    event = {"command_line": "powershell.exe -enc dGVzdA=="}
    matched, reason = _event_matches_rule(event, rule)
    assert matched
    assert "-enc" in reason or "command_line" in reason


def test_all_condition_requires_all_fields():
    rule = {
        "id": "test_all", "name": "Test All", "severity": "medium",
        "detection": {
            "condition": "all",
            "fields": {
                "event_type": {"equals": "auth_failure"},
                "process_name": {"contains": ["sshd"]},
            },
        },
    }
    partial_event = {"event_type": "auth_failure", "process_name": "httpd"}
    matched, _ = _event_matches_rule(partial_event, rule)
    assert not matched

    full_event = {"event_type": "auth_failure", "process_name": "sshd"}
    matched, _ = _event_matches_rule(full_event, rule)
    assert matched
