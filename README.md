# Purple Team Attack Simulator

[![CI](https://github.com/your-username/purple-team-attack-simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/purple-team-attack-simulator/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Purple Team Attack Simulator is a local defensive cybersecurity lab designed to emulate controlled adversary-like behaviors through synthetic logs, validate detection rules, map results to MITRE ATT&CK, and generate SOC-ready reports.

---

## Why this project matters

Security teams need a safe way to validate whether their detection logic works before a real incident occurs. This project provides a controlled local environment to simulate attacker-like patterns, generate telemetry, validate detections, and report coverage gaps.

**Use cases:**
- Validate SIEM detection rules before deployment
- Train SOC analysts with realistic log data
- Run purple team exercises without touching production systems
- Build a personal cybersecurity portfolio project

---

## Safety-first design

This tool does not exploit systems, steal credentials, deploy malware, bypass security tools, or perform destructive actions. It generates **synthetic telemetry** for authorized defensive testing and education only.

See [SAFETY.md](SAFETY.md) for full details.

---

## Features

- **10 attack scenarios** covering Windows, Linux, Web, Network and Identity platforms
- **Synthetic log generation** — realistic JSONL events, zero system impact
- **YAML detection rules** with `contains`, `equals`, `regex`, `not_contains` matchers and `all/any` conditions
- **MITRE ATT&CK mapping** for all scenarios and rules
- **FastAPI REST backend** with automatic OpenAPI documentation
- **Typer CLI** (`pts`) with list, run, validate, coverage, report, clean commands
- **React/TypeScript dashboard** with 5 pages (Dashboard, Scenarios, Runs, Run Details, Coverage)
- **HTML, Markdown and JSON reports** with Jinja2 templates
- **Coverage calculator** — tracks which techniques are covered, not detected, or not tested
- **Pytest test suite** — 25+ tests
- **Docker Compose** for one-command deployment
- **GitHub Actions CI** for automated testing and build validation

---

## Architecture

```
CLI (pts)  ──→  FastAPI Backend  ──→  SQLite DB
                     │
              Services Layer
         ┌────────────────────────┐
         │ scenario_runner        │
         │ synthetic_log_gen      │
         │ detection_engine       │
         │ report_generator       │
         │ coverage_calculator    │
         └────────────────────────┘
                     │
              YAML Files             React Frontend
         scenarios/*.yml  ──→    Dashboard / Scenarios
         rules/*.yml       ──→   Runs / Coverage / Reports
```

Full architecture: [docs/architecture.md](docs/architecture.md)

---

## Stack

| Layer | Technology |
|---|---|
| Backend API | Python 3.11, FastAPI, Uvicorn |
| ORM / DB | SQLAlchemy 2.0, SQLite |
| Validation | Pydantic v2 |
| CLI | Typer + Rich |
| Scenarios/Rules | PyYAML |
| Reports | Jinja2 |
| Tests | Pytest, HTTPX |
| Frontend | React 18, TypeScript, Vite |
| DevOps | Docker, Docker Compose, Makefile, GitHub Actions |

---

## Local Installation

### Prerequisites
- Python 3.11+
- Node.js 20+
- pip

### Setup

```bash
git clone https://github.com/your-username/purple-team-attack-simulator.git
cd purple-team-attack-simulator

# Install backend + frontend
make setup

# Run the demo
make demo
```

### Backend only

```bash
cd backend
pip install -e .
pts list-scenarios
```

---

## Docker

```bash
# Build and start both services
make docker-up
# or:
docker compose up --build
```

| Service | URL |
|---|---|
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Frontend Dashboard | http://localhost:5173 |

---

## CLI Usage (`pts`)

```bash
# List all available scenarios
pts list-scenarios

# Show a specific scenario
pts show-scenario suspicious-powershell

# Run a single scenario
pts run suspicious-powershell

# Run all scenarios
pts run-all

# Validate detection results
pts validate latest
pts validate 20260101-101530-suspicious-powershell

# Check MITRE ATT&CK coverage
pts coverage

# Generate reports
pts report latest --format html
pts report latest --format md
pts report latest --format json

# Clean generated files
pts clean

# Start the API server
pts serve-api
```

Example output:
```
✓ Scenario executed successfully
  Run ID         : 20260101-101530-suspicious-powershell
  Generated logs : 6 events
  Log file       : generated_logs/20260101-101530-suspicious-powershell.jsonl
  Alerts         : 1
  Coverage       : covered
```

---

## API Usage

Full reference: [docs/api_reference.md](docs/api_reference.md)

```bash
# List scenarios
curl http://localhost:8000/api/scenarios

# Run a scenario
curl -X POST http://localhost:8000/api/scenarios/suspicious-powershell/run

# Get coverage
curl http://localhost:8000/api/coverage

# Download HTML report
curl http://localhost:8000/api/reports/{run_id}?format=html -o report.html
```

---

## Dashboard

The React dashboard provides:
- **Dashboard**: KPIs, recent runs, alerts by severity, coverage overview
- **Scenarios**: Table with Run button for each scenario
- **Runs**: History of all simulation runs with status
- **Run Details**: Timeline, alerts, validation, export links
- **Coverage**: MITRE ATT&CK coverage matrix

---

## Scenarios

| ID | Platform | MITRE | Severity |
|---|---|---|---|
| suspicious-powershell | Windows | T1059.001 | High |
| ssh-bruteforce | Linux | T1110 | High |
| new-admin-user | Windows | T1136 | High |
| scheduled-task-creation | Windows | T1053 | Medium |
| temp-process-execution | Windows | T1204 | High |
| suspicious-curl-download | Linux | T1105 | High |
| process-masquerading | Windows | T1036 | High |
| abnormal-login-time | Identity | T1078 | Medium |
| webshell-like-request | Web | T1505.003 | Critical |
| dns-exfil-pattern | Network | T1048 | High |

Full catalog: [docs/scenarios_catalog.md](docs/scenarios_catalog.md)

---

## Report Example

Generated reports include:
- Executive summary
- Scenario details (platform, MITRE tactic/technique, severity)
- Simulation result (run ID, timestamps, log count, alert count)
- Detection logic (matched rule, fields, reason)
- Event timeline table
- Alert table
- Defensive recommendations
- Limitations notice

---

## MITRE ATT&CK Mapping

Full mapping: [docs/mitre_mapping.md](docs/mitre_mapping.md)

Tactics covered: Execution, Persistence, Credential Access, Defense Evasion, Initial Access, Command and Control, Exfiltration

---

## Security & Limits

- All simulations are **synthetic** — no real commands are executed
- No network connections are made to external targets
- No system files are modified
- All generated artifacts are in `generated_logs/`, `generated_reports/`, `lab_sandbox/`
- `pts clean` removes all generated files

See [SAFETY.md](SAFETY.md) for the complete security policy.

---

## Tests

```bash
# Run all tests
make test
# or:
cd backend && python -m pytest tests/ -v
```

Test coverage:
- Scenario YAML loading and validation
- Rule YAML loading and validation
- Synthetic log generation for all 10 scenarios
- Detection engine: positive detection for all 10 scenarios
- Detection engine: no false positives on benign events
- matcher logic (contains, equals, all/any conditions)
- Scenario runner (DB records, JSONL files)
- Report generation (HTML, Markdown, JSON)
- Coverage calculation
- API endpoints (health, scenarios, runs, validate, coverage)

---

## Roadmap

- [ ] Export rules in Sigma format
- [ ] Integration connector for Elastic/OpenSearch
- [ ] Splunk HTTP Event Collector (HEC) integration
- [ ] Microsoft Sentinel analytics rule export
- [ ] Import real authorized log files for testing
- [ ] Visual MITRE ATT&CK matrix navigator
- [ ] SOC maturity scoring across scenarios
- [ ] Multi-environment profiles (cloud, OT, mobile)
- [ ] Optional JWT authentication for dashboard
- [ ] Additional scenarios: Living-off-the-Land, Kerberoasting patterns, Supply chain patterns

---

## Documentation

| File | Description |
|---|---|
| [docs/architecture.md](docs/architecture.md) | System architecture and data flow |
| [docs/demo_scenario.md](docs/demo_scenario.md) | Step-by-step walkthrough |
| [docs/detection_logic.md](docs/detection_logic.md) | Rule format, matchers, conditions |
| [docs/scenarios_catalog.md](docs/scenarios_catalog.md) | Full scenario catalog |
| [docs/mitre_mapping.md](docs/mitre_mapping.md) | MITRE ATT&CK technique mapping |
| [docs/api_reference.md](docs/api_reference.md) | REST API documentation |
| [SAFETY.md](SAFETY.md) | Security policy and authorized use |
| [SUIVI_PROJET.md](SUIVI_PROJET.md) | Project build journal |

---

## License

MIT — see [LICENSE](LICENSE).

Designed for SOC training, purple team exercises, and defensive security education.
**Authorized lab environments only.**
