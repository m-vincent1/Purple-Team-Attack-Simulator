"""Detection engine: applies YAML rules against log events."""

import re
from typing import Any

from app.services.scenario_loader import load_all_rules


def _match_value(event_val: str | None, matcher: dict | list | str) -> bool:
    if event_val is None:
        return False
    event_str = str(event_val).lower()

    if isinstance(matcher, str):
        return event_str == matcher.lower()

    if isinstance(matcher, list):
        return any(_match_value(event_val, m) for m in matcher)

    if isinstance(matcher, dict):
        results = []
        if "equals" in matcher:
            vals = matcher["equals"]
            if isinstance(vals, list):
                results.append(any(event_str == str(v).lower() for v in vals))
            else:
                results.append(event_str == str(vals).lower())
        if "contains" in matcher:
            vals = matcher["contains"]
            if not isinstance(vals, list):
                vals = [vals]
            results.append(any(str(v).lower() in event_str for v in vals))
        if "not_contains" in matcher:
            vals = matcher["not_contains"]
            if not isinstance(vals, list):
                vals = [vals]
            results.append(all(str(v).lower() not in event_str for v in vals))
        if "regex" in matcher:
            patterns = matcher["regex"]
            if not isinstance(patterns, list):
                patterns = [patterns]
            results.append(any(re.search(p, event_val, re.IGNORECASE) for p in patterns))
        return all(results) if results else False

    return False


def _event_matches_rule(event: dict[str, Any], rule: dict[str, Any]) -> tuple[bool, str]:
    detection = rule.get("detection", {})
    condition = detection.get("condition", "any").lower()
    fields = detection.get("fields", {})

    if not fields:
        return False, ""

    field_results = []
    matched_fields = []

    for field_name, matcher in fields.items():
        event_val = event.get(field_name)
        matched = _match_value(event_val, matcher)
        field_results.append(matched)
        if matched:
            matched_fields.append(f"{field_name}={event_val!r}")

    if condition == "all":
        triggered = all(field_results)
    else:  # any
        triggered = any(field_results)

    reason = f"Matched fields: {', '.join(matched_fields)}" if triggered else ""
    return triggered, reason


def run_detection(
    events: list[dict[str, Any]],
    rules: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Run all rules against all events. Returns list of alert dicts."""
    if rules is None:
        rules = load_all_rules()

    alerts = []
    for event_idx, event in enumerate(events):
        for rule in rules:
            if not rule.get("enabled", True):
                continue
            matched, reason = _event_matches_rule(event, rule)
            if matched:
                mitre = rule.get("mitre", {})
                alerts.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "severity": rule.get("severity", "medium"),
                    "event_index": event_idx,
                    "reason": reason,
                    "mitre_technique_id": mitre.get("technique_id", ""),
                    "mitre_tactic": mitre.get("tactic", ""),
                    "event_timestamp": event.get("timestamp"),
                })
    return alerts
