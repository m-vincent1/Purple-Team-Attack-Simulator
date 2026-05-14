# Architecture — Purple Team Attack Simulator

## Overview

```
┌─────────────┐     HTTP/REST     ┌──────────────────────────────────────┐
│   Browser   │ ←───────────────→ │          Frontend (React/Vite)        │
│  Dashboard  │                   │  Dashboard · Scenarios · Runs · Cov.  │
└─────────────┘                   └──────────────────────────────────────┘
                                               ↕ /api/*
                                   ┌──────────────────────────────────────┐
                                   │        Backend (FastAPI)              │
                                   │  ┌──────────┐  ┌──────────────────┐  │
                                   │  │   API    │  │    Services      │  │
                                   │  │  Routes  │  │ scenario_runner  │  │
                                   │  └──────────┘  │ detection_engine │  │
                                   │                │ report_generator │  │
                                   │  ┌──────────┐  │ coverage_calc.  │  │
                                   │  │  Models  │  └──────────────────┘  │
                                   │  │ SQLAlch. │                         │
                                   │  └──────────┘  ┌──────────────────┐  │
                                   │                │     YAML Files   │  │
                                   │  ┌──────────┐  │ scenarios/*.yml  │  │
                                   │  │  SQLite  │  │ rules/*.yml      │  │
                                   │  └──────────┘  └──────────────────┘  │
                                   └──────────────────────────────────────┘
                                               ↕
                                   ┌──────────────────────────────────────┐
                                   │           CLI (Typer/Rich)            │
                                   │  pts list-scenarios · run · report   │
                                   └──────────────────────────────────────┘
```

## Data Flow

1. **Scenario loading**: YAML files in `backend/scenarios/` are parsed by `scenario_loader.py` and seeded into SQLite at startup.
2. **Rule loading**: YAML files in `backend/rules/` are parsed similarly and seeded as `DetectionRule` records.
3. **Simulation run**: `scenario_runner.py` calls `synthetic_log_generator.py` to produce fake log events, stores them as `LogEvent` records, then calls `detection_engine.py` to apply rules.
4. **Detection**: `detection_engine.py` evaluates each event against each rule using field matchers (contains, equals, regex, not_contains) and conditions (all/any). Matches create `Alert` records.
5. **Report generation**: `report_generator.py` queries the DB for run data and renders Jinja2 templates to HTML/Markdown, or serializes to JSON.
6. **Coverage calculation**: `coverage_calculator.py` aggregates run results across all scenarios to compute a MITRE ATT&CK coverage rate.

## Backend Design Choices

- **FastAPI**: Chosen for automatic OpenAPI documentation, Pydantic validation, and async support.
- **SQLAlchemy 2.0**: Declarative models with type annotations for clarity and IDE support.
- **SQLite**: Zero-configuration local database appropriate for single-user lab environments.
- **Pydantic v2**: Strict schema validation for all API inputs and outputs.
- **Synthetic-only simulation**: The log generator never executes system calls — all events are Python dicts.

## Frontend Design Choices

- **React 18 + TypeScript**: Type safety catches API contract mismatches at build time.
- **Vite**: Fast HMR for development, optimized production builds.
- **No external UI library**: Intentional — keeps the dependency footprint small and avoids bundle bloat.
- **React Router v6**: Client-side routing with nested layouts.

## Database Schema

```
scenarios          simulation_runs      log_events
─────────          ───────────────      ──────────
id (PK)            id (PK)              id (PK, auto)
name               scenario_id (FK)     run_id (FK)
description        status               timestamp
platform           started_at           source / host / user
tactic             finished_at          event_type / event_id
technique_id       mode                 process_name / command_line
severity           result_summary       src_ip / dst_ip
expected_detection                      raw_message / event_json

detection_rules    alerts
───────────────    ──────
id (PK)            id (PK, auto)
name               run_id (FK)
severity           rule_id
tactic             title / severity
technique_id       matched_event_id (FK)
enabled            reason / mitre_*
```

## Scenarios / Rules Separation

Scenarios define *what to simulate* (platform, MITRE mapping, log profile).
Rules define *what to detect* (field matchers, conditions, false positive notes).
This separation allows rules to be reused across scenarios and allows scenarios to evolve independently of detection logic.
