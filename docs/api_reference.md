# API Reference

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## Health

### GET /health
Returns service status.

**Response:**
```json
{ "status": "ok", "service": "purple-team-attack-simulator" }
```

## Scenarios

### GET /api/scenarios
List all enabled scenarios.

### GET /api/scenarios/{scenario_id}
Get a specific scenario by ID.

### POST /api/scenarios/{scenario_id}/run
Execute a scenario simulation. Returns run summary.

**Response:**
```json
{
  "run_id": "20260101-101530-suspicious-powershell",
  "scenario_id": "suspicious-powershell",
  "events_generated": 6,
  "alerts_count": 1,
  "detected": true,
  "coverage_status": "covered",
  "log_file": "/path/to/generated_logs/..."
}
```

## Runs

### GET /api/runs
List all simulation runs (newest first).

### POST /api/runs/run-all
Execute all enabled scenarios.

### GET /api/runs/{run_id}
Get a specific run by ID.

### GET /api/runs/{run_id}/logs
Get all log events for a run.

### GET /api/runs/{run_id}/alerts
Get all alerts generated for a run.

### POST /api/runs/{run_id}/validate
Validate detection results for a run.

**Response:**
```json
{
  "run_id": "...",
  "scenario_id": "suspicious-powershell",
  "expected_detection": "suspicious_powershell_rule",
  "detected": true,
  "alerts_count": 1,
  "coverage_status": "covered"
}
```

## Coverage

### GET /api/coverage
Get MITRE ATT&CK coverage statistics.

**Response:**
```json
{
  "total_scenarios": 10,
  "total_techniques": 10,
  "total_tactics": 7,
  "detected_scenarios": 8,
  "undetected_scenarios": 0,
  "coverage_rate": 80.0,
  "alerts_by_severity": { "high": 5, "medium": 2, "critical": 1 },
  "technique_coverage": [...]
}
```

## Reports

### GET /api/reports/{run_id}?format=html
### GET /api/reports/{run_id}?format=md
### GET /api/reports/{run_id}?format=json

Generate and download a report for a run. Supported formats: `html`, `md`, `json`.
