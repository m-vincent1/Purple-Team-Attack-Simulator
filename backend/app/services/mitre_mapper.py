"""Maps scenarios and rules to MITRE ATT&CK framework entries."""

from typing import Any


MITRE_CATALOG: dict[str, dict[str, str]] = {
    "T1059.001": {"tactic": "Execution", "name": "PowerShell"},
    "T1110": {"tactic": "Credential Access", "name": "Brute Force"},
    "T1136": {"tactic": "Persistence", "name": "Create Account"},
    "T1053": {"tactic": "Execution", "name": "Scheduled Task/Job"},
    "T1204": {"tactic": "Execution", "name": "User Execution"},
    "T1105": {"tactic": "Command and Control", "name": "Ingress Tool Transfer"},
    "T1036": {"tactic": "Defense Evasion", "name": "Masquerading"},
    "T1078": {"tactic": "Initial Access", "name": "Valid Accounts"},
    "T1505.003": {"tactic": "Persistence", "name": "Web Shell"},
    "T1048": {"tactic": "Exfiltration", "name": "Exfiltration Over Alternative Protocol"},
    "T1071.004": {"tactic": "Command and Control", "name": "DNS"},
}


def get_technique_info(technique_id: str) -> dict[str, str]:
    return MITRE_CATALOG.get(technique_id, {"tactic": "Unknown", "name": technique_id})


def build_coverage_matrix(
    scenarios: list[Any], runs: list[Any], alerts: list[Any]
) -> list[dict]:
    alerted_run_ids = {a.run_id for a in alerts}
    run_by_scenario: dict[str, list] = {}
    for run in runs:
        run_by_scenario.setdefault(run.scenario_id, []).append(run)

    matrix = []
    for scenario in scenarios:
        scenario_runs = run_by_scenario.get(scenario.id, [])
        if not scenario_runs:
            status = "not_tested"
        else:
            detected = any(r.id in alerted_run_ids for r in scenario_runs)
            status = "covered" if detected else "not_detected"
        matrix.append({
            "scenario_id": scenario.id,
            "scenario_name": scenario.name,
            "technique_id": scenario.technique_id,
            "technique_name": scenario.technique_name,
            "tactic": scenario.tactic,
            "severity": scenario.severity,
            "detection_rule": scenario.expected_detection,
            "status": status,
        })
    return matrix
