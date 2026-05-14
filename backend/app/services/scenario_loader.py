from pathlib import Path
from typing import Any
import yaml

from app.core.config import settings


def load_scenario_yaml(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _validate_scenario(data, path)
    return data


def _validate_scenario(data: dict, path: Path) -> None:
    required = ["id", "name", "description", "platform", "severity", "mitre"]
    for field in required:
        if field not in data:
            raise ValueError(f"Scenario {path.name} missing required field: {field}")


def load_all_scenarios() -> list[dict[str, Any]]:
    scenarios = []
    scenarios_dir = settings.scenarios_path
    if not scenarios_dir.exists():
        return scenarios
    for yml_file in sorted(scenarios_dir.glob("*.yml")):
        try:
            scenarios.append(load_scenario_yaml(yml_file))
        except Exception as e:
            print(f"[WARN] Failed to load scenario {yml_file.name}: {e}")
    return scenarios


def load_rule_yaml(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _validate_rule(data, path)
    return data


def _validate_rule(data: dict, path: Path) -> None:
    required = ["id", "name", "severity", "detection"]
    for field in required:
        if field not in data:
            raise ValueError(f"Rule {path.name} missing required field: {field}")


def load_all_rules() -> list[dict[str, Any]]:
    rules = []
    rules_dir = settings.rules_path
    if not rules_dir.exists():
        return rules
    for yml_file in sorted(rules_dir.glob("*.yml")):
        try:
            rules.append(load_rule_yaml(yml_file))
        except Exception as e:
            print(f"[WARN] Failed to load rule {yml_file.name}: {e}")
    return rules
