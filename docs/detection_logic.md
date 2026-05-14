# Detection Logic

## Rule Format

Detection rules are defined in YAML files in `backend/rules/`. Each rule follows this schema:

```yaml
id: rule_unique_id
name: Human readable name
description: What this rule detects
severity: critical | high | medium | low
enabled: true | false
mitre:
  tactic: Execution
  technique_id: T1059.001
  technique_name: PowerShell
logsource:
  source: windows_security
  event_type: process_creation
detection:
  condition: any | all
  fields:
    field_name:
      contains:
        - value1
        - value2
    other_field:
      equals: exact_value
false_positives:
  - Description of known false positive scenario
recommendation: Defensive action recommended when this rule fires.
```

## Conditions

### `any` condition
Triggers if **at least one** field matcher is satisfied.

```yaml
detection:
  condition: any
  fields:
    command_line:
      contains: ["-enc", "EncodedCommand"]
    process_name:
      contains: ["powershell"]
```
This fires if the command_line contains `-enc` OR `EncodedCommand` OR the process_name contains `powershell`.

### `all` condition
Triggers only if **all** field matchers are satisfied simultaneously.

```yaml
detection:
  condition: all
  fields:
    event_type:
      equals: auth_failure
    process_name:
      contains: ["sshd"]
```
Both conditions must match on the same event.

## Matchers

| Matcher | Description | Example |
|---|---|---|
| `equals` | Exact string match (case-insensitive) | `equals: auth_failure` |
| `contains` | Substring match on one or more values | `contains: ["-enc", "FromBase64"]` |
| `not_contains` | Absence of substring (all values must be absent) | `not_contains: ["System32"]` |
| `regex` | Regular expression match | `regex: "cmd\\.exe.*powershell"` |

All matchers are case-insensitive.

## Field Matching

Fields in the `detection.fields` block correspond to `LogEvent` model attributes:
- `source`, `host`, `user`
- `event_type`, `event_id`
- `process_name`, `command_line`
- `src_ip`, `dst_ip`
- `raw_message`

## False Positives

The `false_positives` list in each rule documents known benign scenarios that might trigger the rule. This list is:
- Displayed in generated reports
- Available via the API
- Not used programmatically (no automatic suppression)

## Recommendations

The `recommendation` field provides SOC analysts with concrete defensive actions. These are included in all generated reports.
