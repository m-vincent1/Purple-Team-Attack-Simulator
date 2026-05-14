import pytest
from app.services.scenario_loader import load_all_scenarios, load_all_rules


def test_load_all_scenarios_returns_list():
    scenarios = load_all_scenarios()
    assert isinstance(scenarios, list)


def test_load_all_scenarios_count():
    scenarios = load_all_scenarios()
    assert len(scenarios) == 10, f"Expected 10 scenarios, got {len(scenarios)}"


def test_scenarios_have_required_fields():
    scenarios = load_all_scenarios()
    for s in scenarios:
        assert "id" in s
        assert "name" in s
        assert "mitre" in s
        assert "severity" in s


def test_scenarios_have_mitre_fields():
    scenarios = load_all_scenarios()
    for s in scenarios:
        mitre = s["mitre"]
        assert "tactic" in mitre
        assert "technique_id" in mitre


def test_load_all_rules_returns_list():
    rules = load_all_rules()
    assert isinstance(rules, list)


def test_load_all_rules_count():
    rules = load_all_rules()
    assert len(rules) == 10, f"Expected 10 rules, got {len(rules)}"


def test_rules_have_required_fields():
    rules = load_all_rules()
    for r in rules:
        assert "id" in r
        assert "name" in r
        assert "severity" in r
        assert "detection" in r


def test_rule_detection_has_fields():
    rules = load_all_rules()
    for r in rules:
        detection = r["detection"]
        assert "fields" in detection
        assert "condition" in detection
