"""Purple Team Simulator CLI — pts"""

import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

app = typer.Typer(
    name="pts",
    help="Purple Team Attack Simulator — local defensive simulation CLI",
    no_args_is_help=True,
)
console = Console()


def _get_db():
    # Ensure we're running from the backend directory or that the DB path is resolved
    from app.core.database import init_db, SessionLocal
    init_db()
    return SessionLocal()


def _seed_db():
    db = _get_db()
    try:
        from app.main import _seed_scenarios_and_rules
        from app.core.database import SessionLocal
        _seed_db_internal()
    finally:
        db.close()


def _seed_db_internal():
    from app.core.database import SessionLocal, init_db
    from app.services.scenario_loader import load_all_scenarios, load_all_rules
    from app.models.scenario import Scenario
    from app.models.detection import DetectionRule
    init_db()
    db = SessionLocal()
    try:
        for data in load_all_scenarios():
            if not db.get(Scenario, data["id"]):
                mitre = data.get("mitre", {})
                db.add(Scenario(
                    id=data["id"], name=data["name"],
                    description=data.get("description", ""),
                    platform=data.get("platform", "generic"),
                    tactic=mitre.get("tactic", ""),
                    technique_id=mitre.get("technique_id", ""),
                    technique_name=mitre.get("technique_name", ""),
                    severity=data.get("severity", "medium"),
                    mode=data.get("mode", "synthetic"),
                    expected_detection=data.get("expected_detection"),
                ))
        for data in load_all_rules():
            if not db.get(DetectionRule, data["id"]):
                mitre = data.get("mitre", {})
                db.add(DetectionRule(
                    id=data["id"], name=data["name"],
                    description=data.get("description", ""),
                    severity=data.get("severity", "medium"),
                    tactic=mitre.get("tactic", ""),
                    technique_id=mitre.get("technique_id", ""),
                ))
        db.commit()
    finally:
        db.close()


@app.command("list-scenarios")
def list_scenarios():
    """List all available simulation scenarios."""
    _seed_db_internal()
    from app.core.database import SessionLocal
    from app.models.scenario import Scenario
    db = SessionLocal()
    try:
        scenarios = db.query(Scenario).filter(Scenario.enabled == True).all()  # noqa: E712
        if not scenarios:
            console.print("[yellow]No scenarios found. Make sure YAML files exist in backend/scenarios/[/yellow]")
            return
        table = Table(title="Available Scenarios", show_lines=False)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Platform", style="blue")
        table.add_column("Tactic", style="magenta")
        table.add_column("Technique", style="green")
        table.add_column("Severity", style="yellow")
        for s in scenarios:
            table.add_row(s.id, s.name, s.platform, s.tactic, s.technique_id, s.severity)
        console.print(table)
        console.print(f"\n[bold]Total: {len(scenarios)} scenarios[/bold]")
    finally:
        db.close()


@app.command("show-scenario")
def show_scenario(scenario_id: str):
    """Show details for a specific scenario."""
    _seed_db_internal()
    from app.core.database import SessionLocal
    from app.models.scenario import Scenario
    db = SessionLocal()
    try:
        scenario = db.get(Scenario, scenario_id)
        if not scenario:
            console.print(f"[red]Scenario not found: {scenario_id}[/red]")
            raise typer.Exit(1)
        console.print(f"\n[bold cyan]{scenario.name}[/bold cyan]")
        console.print(f"  ID          : {scenario.id}")
        console.print(f"  Description : {scenario.description}")
        console.print(f"  Platform    : {scenario.platform}")
        console.print(f"  Tactic      : {scenario.tactic}")
        console.print(f"  Technique   : {scenario.technique_id} — {scenario.technique_name}")
        console.print(f"  Severity    : {scenario.severity}")
        console.print(f"  Mode        : {scenario.mode}")
        console.print(f"  Detection   : {scenario.expected_detection}")
    finally:
        db.close()


@app.command("run")
def run_scenario(scenario_id: str):
    """Execute a simulation scenario and generate synthetic logs."""
    _seed_db_internal()
    from app.core.database import SessionLocal
    from app.services.scenario_runner import run_scenario as _run
    db = SessionLocal()
    try:
        console.print(f"\n[bold]Running scenario:[/bold] {scenario_id}")
        with console.status("Generating synthetic events..."):
            result = _run(scenario_id, db)
        console.print(f"[green]✓ Scenario executed successfully[/green]")
        console.print(f"  Run ID         : {result['run_id']}")
        console.print(f"  Generated logs : {result['events_generated']} events")
        console.print(f"  Log file       : {result['log_file']}")
        console.print(f"  Alerts         : {result['alerts_count']}")
        console.print(f"  Coverage       : [bold]{result['coverage_status']}[/bold]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    finally:
        db.close()


@app.command("run-all")
def run_all():
    """Execute all enabled scenarios."""
    _seed_db_internal()
    from app.core.database import SessionLocal
    from app.models.scenario import Scenario
    from app.services.scenario_runner import run_scenario as _run
    db = SessionLocal()
    try:
        scenarios = db.query(Scenario).filter(Scenario.enabled == True).all()  # noqa: E712
        console.print(f"\n[bold]Running all {len(scenarios)} scenarios...[/bold]\n")
        covered = 0
        for s in scenarios:
            try:
                result = _run(s.id, db)
                status = "[green]covered[/green]" if result["coverage_status"] == "covered" else "[red]not_detected[/red]"
                console.print(f"  ✓ {s.id:<40} alerts: {result['alerts_count']}  {status}")
                if result["coverage_status"] == "covered":
                    covered += 1
            except Exception as e:
                console.print(f"  ✗ {s.id:<40} [red]FAILED: {e}[/red]")
        console.print(f"\n[bold]Coverage: {covered}/{len(scenarios)} scenarios detected[/bold]")
    finally:
        db.close()


@app.command("validate")
def validate(run_id: str):
    """Validate detection results for a run (use 'latest' for most recent)."""
    _seed_db_internal()
    from app.core.database import SessionLocal
    from app.models.run import SimulationRun
    from app.models.alert import Alert
    from app.models.scenario import Scenario
    db = SessionLocal()
    try:
        if run_id == "latest":
            run = db.query(SimulationRun).order_by(SimulationRun.started_at.desc()).first()
            if not run:
                console.print("[red]No runs found.[/red]")
                raise typer.Exit(1)
            run_id = run.id
        else:
            run = db.get(SimulationRun, run_id)
        if not run:
            console.print(f"[red]Run not found: {run_id}[/red]")
            raise typer.Exit(1)
        scenario = db.get(Scenario, run.scenario_id)
        alerts = db.query(Alert).filter(Alert.run_id == run_id).all()
        detected_rules = {a.rule_id for a in alerts}
        expected = scenario.expected_detection if scenario else None
        detected = (expected in detected_rules) if expected else len(detected_rules) > 0
        status = "covered" if detected else "not_detected"
        console.print(f"\n[bold]Validation Result[/bold]")
        console.print(f"  Run ID            : {run_id}")
        console.print(f"  Scenario          : {run.scenario_id}")
        console.print(f"  Expected rule     : {expected}")
        console.print(f"  Detected          : {'[green]YES[/green]' if detected else '[red]NO[/red]'}")
        console.print(f"  Alerts count      : {len(alerts)}")
        console.print(f"  Coverage status   : [bold]{status}[/bold]")
    finally:
        db.close()


@app.command("coverage")
def coverage():
    """Display MITRE ATT&CK coverage summary."""
    _seed_db_internal()
    from app.core.database import SessionLocal
    from app.services.coverage_calculator import calculate_coverage
    db = SessionLocal()
    try:
        cov = calculate_coverage(db)
        console.print(f"\n[bold]MITRE ATT&CK Coverage Report[/bold]\n")
        console.print(f"  Total scenarios    : {cov['total_scenarios']}")
        console.print(f"  Techniques covered : {cov['total_techniques']}")
        console.print(f"  Tactics covered    : {cov['total_tactics']}")
        console.print(f"  Detected           : {cov['detected_scenarios']}")
        console.print(f"  Not detected       : {cov['undetected_scenarios']}")
        console.print(f"  Coverage rate      : [bold]{cov['coverage_rate']}%[/bold]")
        if cov["alerts_by_severity"]:
            console.print(f"\n  Alerts by severity:")
            for sev, count in cov["alerts_by_severity"].items():
                console.print(f"    {sev:<12}: {count}")
    finally:
        db.close()


@app.command("report")
def report(
    run_id: str,
    format: str = typer.Option("html", "--format", "-f", help="Report format: html, md, json"),
):
    """Generate a report for a simulation run."""
    _seed_db_internal()
    from app.core.database import SessionLocal
    from app.models.run import SimulationRun
    from app.services.report_generator import generate_report
    db = SessionLocal()
    try:
        if run_id == "latest":
            run = db.query(SimulationRun).order_by(SimulationRun.started_at.desc()).first()
            if not run:
                console.print("[red]No runs found.[/red]")
                raise typer.Exit(1)
            run_id = run.id
        path = generate_report(run_id, format, db)
        console.print(f"[green]✓ Report generated:[/green] {path}")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    finally:
        db.close()


@app.command("clean")
def clean():
    """Remove all generated logs, reports and sandbox files."""
    from app.core.config import settings
    import shutil
    logs_dir = settings.generated_logs_path
    reports_dir = settings.generated_reports_path
    sandbox_dir = settings.lab_sandbox_path

    deleted = 0
    for d, pattern in [(logs_dir, "*.jsonl"), (reports_dir, "*.html"), (reports_dir, "*.md"), (reports_dir, "*.json")]:
        for f in d.glob(pattern):
            f.unlink()
            deleted += 1
    for f in sandbox_dir.iterdir():
        if f.name != ".gitkeep":
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()
            deleted += 1

    console.print(f"[green]✓ Cleaned {deleted} generated files.[/green]")


@app.command("serve-api")
def serve_api(
    host: str = typer.Option("0.0.0.0", help="Host to bind"),
    port: int = typer.Option(8000, help="Port to bind"),
):
    """Start the FastAPI backend server."""
    import uvicorn
    console.print(f"[bold]Starting Purple Team API on {host}:{port}[/bold]")
    uvicorn.run("app.main:app", host=host, port=port, reload=False)


def main():
    app()


if __name__ == "__main__":
    main()
