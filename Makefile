.PHONY: setup install-backend install-frontend run-api run-frontend run-cli-demo demo test lint format clean docker-build docker-up docker-down report

# ── Setup ────────────────────────────────────────────────────────────────────
setup: install-backend install-frontend
	@echo "✓ Setup complete. Run 'make demo' to start."

install-backend:
	cd backend && pip install -e ".[dev]" 2>/dev/null || pip install -e .

install-frontend:
	cd frontend && npm install

# ── Development ──────────────────────────────────────────────────────────────
run-api:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	cd frontend && npm run dev

# ── Demo ─────────────────────────────────────────────────────────────────────
run-cli-demo:
	cd backend && pts list-scenarios
	cd backend && pts run suspicious-powershell
	cd backend && pts coverage

demo:
	@echo "=== Purple Team Attack Simulator — Demo ==="
	cd backend && python -c "\
from app.core.database import init_db, SessionLocal; \
from app.main import _seed_scenarios_and_rules; \
init_db(); \
_seed_scenarios_and_rules(); \
from app.services.scenario_runner import run_scenario; \
from app.services.report_generator import generate_report; \
db = SessionLocal(); \
result = run_scenario('suspicious-powershell', db); \
print('Running scenario: suspicious-powershell'); \
print(f'Generated events: {result[\"events_generated\"]}'); \
print(f'Alerts generated: {result[\"alerts_count\"]}'); \
print(f'Coverage status: {result[\"coverage_status\"]}'); \
path = generate_report(result['run_id'], 'html', db); \
print(f'Report generated: {path}'); \
db.close()"

report:
	cd backend && python -c "\
from app.core.database import init_db, SessionLocal; \
init_db(); \
db = SessionLocal(); \
from app.models.run import SimulationRun; \
run = db.query(SimulationRun).order_by(SimulationRun.started_at.desc()).first(); \
from app.services.report_generator import generate_report; \
path = generate_report(run.id, 'html', db) if run else 'No runs found'; \
print(f'Report: {path}'); \
db.close()"

# ── Tests ────────────────────────────────────────────────────────────────────
test:
	cd backend && python -m pytest tests/ -v --tb=short

# ── Code Quality ─────────────────────────────────────────────────────────────
lint:
	cd backend && python -m ruff check app/ tests/ 2>/dev/null || python -m flake8 app/ tests/ --max-line-length=100
	cd frontend && npx tsc --noEmit

format:
	cd backend && python -m ruff format app/ tests/ 2>/dev/null || python -m black app/ tests/

# ── Cleanup ──────────────────────────────────────────────────────────────────
clean:
	cd backend && python -c "from app.cli.main import clean; clean()" 2>/dev/null || true
	find generated_logs -name "*.jsonl" -delete 2>/dev/null || true
	find generated_reports -name "*.html" -name "*.md" -name "*.json" -delete 2>/dev/null || true
	find backend -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find backend -name "*.pyc" -delete 2>/dev/null || true
	rm -f backend/purple_team.db

# ── Docker ───────────────────────────────────────────────────────────────────
docker-build:
	docker compose build

docker-up:
	docker compose up --build -d
	@echo ""
	@echo "Services started:"
	@echo "  Backend:  http://localhost:8000"
	@echo "  Frontend: http://localhost:5173"
	@echo "  API docs: http://localhost:8000/docs"

docker-down:
	docker compose down
