# Suivi de projet — Purple Team Attack Simulator

## Objectif du projet

Purple Team Attack Simulator est une plateforme locale de simulation d'attaques contrôlées pour les équipes SOC, blue team et purple team. Elle génère des logs synthétiques réalistes, applique des règles de détection YAML, mappe les résultats sur MITRE ATT&CK et produit des rapports de couverture défensive.

Intérêt cyber : valider la couverture de détection avant qu'un vrai incident survienne, sans risque pour les systèmes de production.

## Stack technique

| Technologie | Rôle | Justification |
|---|---|---|
| Python 3.11+ | Backend | Écosystème riche en cybersécurité, typage avancé |
| FastAPI | API REST | Performance, OpenAPI auto, Pydantic intégré |
| Pydantic | Validation | Schémas stricts, serialisation JSON |
| SQLAlchemy | ORM | Abstraction DB, migrations simples |
| SQLite | Base de données | Simplicité locale, zéro configuration |
| Typer | CLI | Interface CLI propre et typée |
| PyYAML | Scénarios/Règles | Format lisible, maintenable |
| Jinja2 | Rapports | Templates HTML/Markdown flexibles |
| Pytest | Tests | Standard Python, fixtures puissantes |
| React + TypeScript | Frontend | Typage strict, composants réutilisables |
| Vite | Build frontend | Rapidité, HMR, configuration minimale |
| Docker + Compose | Conteneurisation | Reproductibilité, déploiement uniforme |
| GitHub Actions | CI | Automatisation tests/build |

## Journal de construction

### Étape 1 — Initialisation du projet
- Objectif : Créer l'arborescence complète et les fichiers de configuration racine
- Fichiers créés : SUIVI_PROJET.md, SAFETY.md, README.md, .gitignore, .env.example, LICENSE, Makefile, docker-compose.yml
- Fichiers modifiés : —
- Choix techniques : SQLite pour simplicité locale, Typer pour CLI propre
- Résultat : Structure de base opérationnelle

### Étape 2 — Architecture backend
- Objectif : Backend FastAPI avec modèles SQLAlchemy et configuration
- Fichiers créés : backend/app/main.py, core/config.py, core/database.py, core/security.py, tous les modèles, tous les schémas
- Fichiers modifiés : —
- Choix techniques : SQLAlchemy 2.0 avec sessions async-ready, Pydantic v2
- Résultat : Backend structuré et typé

### Étape 3 — Moteur de scénarios
- Objectif : Chargeur YAML, moteur de simulation synthétique, générateur de logs
- Fichiers créés : services/scenario_loader.py, services/scenario_runner.py, services/synthetic_log_generator.py, 10 fichiers YAML scénarios
- Choix techniques : Génération synthétique pure, aucune exécution réelle
- Résultat : 10 scénarios fonctionnels

### Étape 4 — Moteur de détection
- Objectif : Moteur de détection avec règles YAML, conditions all/any, matchers
- Fichiers créés : services/detection_engine.py, services/mitre_mapper.py, services/coverage_calculator.py, 10 règles YAML
- Choix techniques : Matchers equals/contains/regex/not_contains, conditions all/any
- Résultat : Détection fonctionnelle sur tous les scénarios

### Étape 5 — API
- Objectif : Endpoints FastAPI REST complets
- Fichiers créés : api/routes_scenarios.py, routes_runs.py, routes_detections.py, routes_reports.py, routes_health.py
- Résultat : API REST complète avec documentation OpenAPI

### Étape 6 — CLI
- Objectif : CLI Typer avec toutes les commandes pts
- Fichiers créés : cli/main.py, pyproject.toml, requirements.txt
- Résultat : CLI pts fonctionnelle

### Étape 7 — Frontend dashboard
- Objectif : Dashboard React/TypeScript sobre et professionnel
- Fichiers créés : src/App.tsx, components/*, pages/*, api/client.ts, types/api.ts
- Résultat : Dashboard avec 5 pages et matrice de couverture

### Étape 8 — Rapports
- Objectif : Génération HTML, Markdown et JSON
- Fichiers créés : services/report_generator.py, reports/templates/report.html.j2, report.md.j2
- Résultat : 3 formats de rapport générés automatiquement

### Étape 9 — Tests et qualité
- Objectif : Suite Pytest complète, 20+ tests
- Fichiers créés : tests/test_scenario_loader.py, test_scenario_runner.py, test_detection_engine.py, test_report_generator.py, test_api.py
- Résultat : 25+ tests, tous passants

### Étape 10 — Documentation finale
- Objectif : README professionnel, docs complètes, CI GitHub Actions
- Fichiers créés : docs/architecture.md, demo_scenario.md, detection_logic.md, scenarios_catalog.md, api_reference.md, mitre_mapping.md, .github/workflows/ci.yml
- Résultat : Documentation complète prête pour GitHub

## Fonctionnalités finales

- 10 scénarios d'attaque YAML (Windows, Linux, Web, Network, IAM)
- 10 règles de détection YAML (equals, contains, regex, not_contains, all/any)
- Moteur de simulation synthétique (aucune action réelle)
- Moteur de détection avec mapping MITRE ATT&CK
- API REST FastAPI avec documentation OpenAPI
- CLI `pts` complète (list, run, validate, coverage, report, clean)
- Dashboard React/TypeScript avec 5 pages
- Rapports HTML, Markdown et JSON
- Calcul de couverture défensive
- Suite de tests Pytest (25+ tests)
- Docker + Docker Compose
- GitHub Actions CI
- Documentation technique complète

## Commandes utiles

```bash
# Installation locale
make setup
make install-backend

# Démonstration
make demo

# Tests
make test

# Docker
make docker-up

# CLI directe
cd backend && pip install -e .
pts list-scenarios
pts run suspicious-powershell
pts report latest --format html
```

## Problèmes connus et limites

- Mode synthétique uniquement : aucune exécution réelle d'attaque
- SQLite local : pas adapté à un déploiement multi-utilisateurs
- Frontend sans authentification (intentionnel pour lab local)
- Les logs générés sont fictifs et ne représentent pas un environnement réel
