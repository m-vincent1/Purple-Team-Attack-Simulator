# Purple Team Attack Simulator

[![CI](https://github.com/m-vincent1/Purple-Team-Attack-Simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/m-vincent1/Purple-Team-Attack-Simulator/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)
[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

> Purple Team Attack Simulator est un laboratoire de cybersécurité défensive local conçu pour simuler des comportements d'attaquants de manière contrôlée, générer des logs synthétiques réalistes, valider des règles de détection, mapper les résultats sur MITRE ATT&CK et produire des rapports de couverture prêts pour un SOC.

---

## Pourquoi ce projet ?

Les équipes de sécurité ont besoin d'un moyen sûr de valider si leur logique de détection fonctionne **avant** qu'un vrai incident ne survienne. Ce projet fournit un environnement local contrôlé pour simuler des comportements d'attaquants, générer de la télémétrie, valider les détections et identifier les lacunes de couverture.

**Cas d'usage :**
- Valider les règles SIEM avant déploiement
- Former les analystes SOC avec des données de logs réalistes
- Effectuer des exercices purple team sans toucher aux systèmes de production
- Projet de portfolio en cybersécurité

---

## Conception orientée sécurité

Cet outil n'exploite pas de systèmes, ne vole pas d'identifiants, ne déploie pas de malware, ne contourne pas les outils de sécurité et n'effectue aucune action destructrice. Il génère uniquement de la **télémétrie synthétique** pour des tests défensifs autorisés et à des fins éducatives.

Voir [SAFETY.md](SAFETY.md) pour les détails complets.

---

## Fonctionnalités

- **10 scénarios d'attaque** couvrant Windows, Linux, Web, Réseau et Identité
- **Génération de logs synthétiques** — événements JSONL réalistes, aucun impact système
- **Règles de détection YAML** avec matchers `contains`, `equals`, `regex`, `not_contains` et conditions `all/any`
- **Mapping MITRE ATT&CK** pour tous les scénarios et toutes les règles
- **API REST FastAPI** avec documentation OpenAPI automatique
- **CLI Typer** (`pts`) avec les commandes list, run, validate, coverage, report, clean
- **Dashboard React/TypeScript** avec 5 pages (Tableau de bord, Scénarios, Exécutions, Détails, Couverture)
- **Rapports HTML, Markdown et JSON** via templates Jinja2
- **Calculateur de couverture** — suit quelles techniques sont couvertes, non détectées ou non testées
- **Suite de tests Pytest** — 37 tests
- **Docker Compose** pour un déploiement en une commande
- **GitHub Actions CI** pour les tests et la validation du build

---

## Architecture

```
CLI (pts)  ──→  Backend FastAPI  ──→  Base SQLite
                      │
               Couche Services
        ┌─────────────────────────┐
        │ scenario_runner         │
        │ synthetic_log_generator │
        │ detection_engine        │
        │ report_generator        │
        │ coverage_calculator     │
        └─────────────────────────┘
                      │
               Fichiers YAML          Frontend React
        scenarios/*.yml  ──→    Tableau de bord / Scénarios
        rules/*.yml      ──→    Exécutions / Couverture / Rapports
```

Architecture complète : [docs/architecture.md](docs/architecture.md)

---

## Stack technique

| Couche | Technologie |
|---|---|
| API Backend | Python 3.11, FastAPI, Uvicorn |
| ORM / Base de données | SQLAlchemy 2.0, SQLite |
| Validation | Pydantic v2 |
| CLI | Typer + Rich |
| Scénarios / Règles | PyYAML |
| Rapports | Jinja2 |
| Tests | Pytest, HTTPX |
| Frontend | React 18, TypeScript, Vite |
| DevOps | Docker, Docker Compose, Makefile, GitHub Actions |

---

## Installation locale

### Prérequis
- Python 3.11+
- Node.js 20+
- pip

### Installation rapide

```bash
git clone https://github.com/m-vincent1/Purple-Team-Attack-Simulator.git
cd Purple-Team-Attack-Simulator

# Installer le backend + frontend
make setup

# Lancer la démo
make demo
```

### Backend seul

```bash
cd backend
pip install -e .
pts list-scenarios
```

---

## Docker

```bash
# Construire et démarrer les deux services
make docker-up
# ou :
docker compose up --build
```

| Service | URL |
|---|---|
| API Backend | http://localhost:8000 |
| Documentation API (Swagger) | http://localhost:8000/docs |
| Dashboard Frontend | http://localhost:5173 |

---

## Utilisation de la CLI (`pts`)

```bash
# Lister tous les scénarios disponibles
pts list-scenarios

# Afficher un scénario spécifique
pts show-scenario suspicious-powershell

# Lancer un scénario
pts run suspicious-powershell

# Lancer tous les scénarios
pts run-all

# Valider les résultats de détection
pts validate latest
pts validate 20260101-101530-suspicious-powershell

# Vérifier la couverture MITRE ATT&CK
pts coverage

# Générer des rapports
pts report latest --format html
pts report latest --format md
pts report latest --format json

# Nettoyer les fichiers générés
pts clean

# Démarrer le serveur API
pts serve-api
```

Exemple de sortie :
```
✓ Scénario exécuté avec succès
  Run ID         : 20260101-101530-suspicious-powershell
  Logs générés   : 6 événements
  Fichier log    : generated_logs/20260101-101530-suspicious-powershell.jsonl
  Alertes        : 1
  Couverture     : covered
```

---

## Utilisation de l'API

Référence complète : [docs/api_reference.md](docs/api_reference.md)

```bash
# Lister les scénarios
curl http://localhost:8000/api/scenarios

# Lancer un scénario
curl -X POST http://localhost:8000/api/scenarios/suspicious-powershell/run

# Obtenir la couverture
curl http://localhost:8000/api/coverage

# Télécharger un rapport HTML
curl http://localhost:8000/api/reports/{run_id}?format=html -o rapport.html
```

---

## Dashboard

Le dashboard React propose :
- **Tableau de bord** : KPIs, exécutions récentes, alertes par sévérité, vue d'ensemble de la couverture
- **Scénarios** : tableau avec bouton Exécuter pour chaque scénario
- **Exécutions** : historique de toutes les simulations avec statut
- **Détails d'exécution** : timeline, alertes, validation, liens d'export
- **Couverture** : matrice de couverture MITRE ATT&CK

---

## Scénarios disponibles

| ID | Plateforme | MITRE | Sévérité |
|---|---|---|---|
| suspicious-powershell | Windows | T1059.001 | Haute |
| ssh-bruteforce | Linux | T1110 | Haute |
| new-admin-user | Windows | T1136 | Haute |
| scheduled-task-creation | Windows | T1053 | Moyenne |
| temp-process-execution | Windows | T1204 | Haute |
| suspicious-curl-download | Linux | T1105 | Haute |
| process-masquerading | Windows | T1036 | Haute |
| abnormal-login-time | Identité | T1078 | Moyenne |
| webshell-like-request | Web | T1505.003 | Critique |
| dns-exfil-pattern | Réseau | T1048 | Haute |

Catalogue complet : [docs/scenarios_catalog.md](docs/scenarios_catalog.md)

---

## Exemple de rapport

Les rapports générés contiennent :
- Résumé exécutif
- Détails du scénario (plateforme, tactique/technique MITRE, sévérité)
- Résultat de simulation (Run ID, horodatages, nombre de logs, alertes)
- Logique de détection (règle matchée, champs, raison de l'alerte)
- Timeline des événements
- Tableau des alertes
- Recommandations défensives
- Avertissement de simulation synthétique

---

## Mapping MITRE ATT&CK

Mapping complet : [docs/mitre_mapping.md](docs/mitre_mapping.md)

Tactiques couvertes : Exécution, Persistance, Accès aux identifiants, Évasion de défense, Accès initial, Commande et contrôle, Exfiltration

---

## Sécurité et limites

- Toutes les simulations sont **synthétiques** — aucune commande réelle n'est exécutée
- Aucune connexion réseau vers des cibles externes
- Aucun fichier système n'est modifié
- Tous les artefacts générés sont dans `generated_logs/`, `generated_reports/`, `lab_sandbox/`
- `pts clean` supprime tous les fichiers générés

Voir [SAFETY.md](SAFETY.md) pour la politique de sécurité complète.

---

## Tests

```bash
# Lancer tous les tests
make test
# ou :
cd backend && python -m pytest tests/ -v
```

Couverture des tests :
- Chargement et validation des scénarios YAML
- Chargement et validation des règles YAML
- Génération de logs synthétiques pour les 10 scénarios
- Moteur de détection : détection positive pour les 10 scénarios
- Moteur de détection : aucun faux positif sur événements bénins
- Logique des matchers (contains, equals, conditions all/any)
- Runner de scénarios (enregistrements DB, fichiers JSONL)
- Génération de rapports (HTML, Markdown, JSON)
- Calcul de couverture
- Endpoints API (health, scenarios, runs, validate, coverage)

---

## Roadmap

- [ ] Export des règles au format Sigma
- [ ] Connecteur pour Elastic/OpenSearch
- [ ] Intégration Splunk HTTP Event Collector (HEC)
- [ ] Export de règles analytiques Microsoft Sentinel
- [ ] Import de fichiers de logs réels autorisés
- [ ] Matrice MITRE ATT&CK visuelle
- [ ] Scoring de maturité SOC
- [ ] Profils multi-environnements (cloud, OT, mobile)
- [ ] Authentification JWT optionnelle pour le dashboard
- [ ] Scénarios supplémentaires : Living-off-the-Land, patterns Kerberoasting

---

## Documentation

| Fichier | Description |
|---|---|
| [docs/architecture.md](docs/architecture.md) | Architecture système et flux de données |
| [docs/demo_scenario.md](docs/demo_scenario.md) | Démonstration pas à pas |
| [docs/detection_logic.md](docs/detection_logic.md) | Format des règles, matchers, conditions |
| [docs/scenarios_catalog.md](docs/scenarios_catalog.md) | Catalogue complet des scénarios |
| [docs/mitre_mapping.md](docs/mitre_mapping.md) | Mapping des techniques MITRE ATT&CK |
| [docs/api_reference.md](docs/api_reference.md) | Documentation de l'API REST |
| [SAFETY.md](SAFETY.md) | Politique de sécurité et usage autorisé |
| [SUIVI_PROJET.md](SUIVI_PROJET.md) | Journal de construction du projet |

---

## Licence

MIT — voir [LICENSE](LICENSE).

Conçu pour la formation SOC, les exercices purple team et l'enseignement de la cybersécurité défensive.
**Environnements de laboratoire autorisés uniquement.**
