# Demo Scenario Walkthrough

## Quick Start

```bash
git clone <repo-url>
cd purple-team-attack-simulator
make setup
make demo
```

## What You Should See

After `make demo`:

```
=== Purple Team Attack Simulator — Demo ===
Running scenario: suspicious-powershell
Generated events: 6
Alerts generated: 1
Coverage status: covered
Report generated: generated_reports/20260101-101530-suspicious-powershell.html
```

## Step-by-Step Manual Demo

### 1. List available scenarios
```bash
cd backend
pts list-scenarios
```
Expected output: table with 10 scenarios, their platforms, tactics and MITRE technique IDs.

### 2. Run a specific scenario
```bash
pts run suspicious-powershell
```
Expected output:
```
✓ Scenario executed successfully
  Run ID         : 20260101-101530-suspicious-powershell
  Generated logs : 6 events
  Log file       : generated_logs/20260101-101530-suspicious-powershell.jsonl
  Alerts         : 1
  Coverage       : covered
```

### 3. Validate the run
```bash
pts validate latest
```
Expected output: detected=YES, coverage_status=covered

### 4. Check coverage
```bash
pts coverage
```
Expected output: coverage rate based on how many scenarios have been run.

### 5. Generate a report
```bash
pts report latest --format html
```
Opens or saves an HTML report in `generated_reports/`.

### 6. Run all scenarios
```bash
pts run-all
```
Runs all 10 scenarios in sequence, showing coverage results.

### 7. Launch the API
```bash
pts serve-api
# or: uvicorn app.main:app --reload
```
Then visit `http://localhost:8000/docs` for the interactive API.

### 8. Launch the dashboard
```bash
# in another terminal:
cd frontend && npm run dev
```
Then visit `http://localhost:5173`.

### 9. Docker (all-in-one)
```bash
make docker-up
```
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

### 10. Clean up
```bash
pts clean
# or: make clean
```
