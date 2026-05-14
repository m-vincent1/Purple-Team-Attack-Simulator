# Prompt complet pour Claude Code / Codex — Purple Team Attack Simulator

Copie-colle tout ce fichier dans Claude Code, Codex ou un agent de génération de code.

---

## Rôle de l'agent

Tu es un ingénieur logiciel senior spécialisé en cybersécurité défensive, blue team, purple team, détection SOC, architecture produit, qualité logicielle et documentation professionnelle.

Tu dois créer un projet GitHub complet, propre, professionnel et directement valorisable dans un portfolio cybersécurité junior/intermédiaire.

Le projet s'appelle :

```text
Purple Team Attack Simulator
```

Nom technique recommandé du dépôt :

```text
purple-team-attack-simulator
```

Objectif : développer une plateforme locale de simulation purple team permettant de générer des scénarios d'attaque contrôlés, produire des logs réalistes, exécuter des règles de détection, mapper les scénarios à MITRE ATT&CK et générer des rapports de couverture défensive.

Le projet doit être défensif, pédagogique, sécurisé et utilisable uniquement dans un environnement local/lab autorisé.

---

## Exigence très importante : fichier de suivi de projet

Dès le début du projet, crée un fichier à la racine :

```text
SUIVI_PROJET.md
```

Ce fichier doit être maintenu à jour pendant toute la construction du projet.

À chaque grande étape, tu dois l'actualiser avec :

- la date ou l'étape courante ;
- l'objectif de l'étape ;
- les fichiers créés ;
- les fichiers modifiés ;
- les choix techniques faits ;
- les fonctionnalités terminées ;
- les tests ajoutés ou exécutés ;
- les problèmes rencontrés ;
- les solutions appliquées ;
- les prochaines étapes.

Le fichier doit permettre à un étudiant ou à un recruteur de comprendre comment le projet a été construit progressivement.

Structure obligatoire de `SUIVI_PROJET.md` :

```markdown
# Suivi de projet — Purple Team Attack Simulator

## Objectif du projet

Résumé du projet et de son intérêt cyber.

## Stack technique

Liste des technologies utilisées et justification.

## Journal de construction

### Étape 1 — Initialisation du projet
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 2 — Architecture backend
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 3 — Moteur de scénarios
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 4 — Moteur de détection
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 5 — API
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 6 — CLI
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 7 — Frontend dashboard
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 8 — Rapports
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 9 — Tests et qualité
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

### Étape 10 — Documentation finale
- Objectif :
- Fichiers créés :
- Fichiers modifiés :
- Choix techniques :
- Résultat :

## Fonctionnalités finales

Liste des fonctionnalités livrées.

## Commandes utiles

Commandes d'installation, de lancement, de test et de démonstration.

## Problèmes connus et limites

Limites volontaires, contraintes de sécurité et améliorations futures.
```

Tu dois mettre ce fichier à jour plusieurs fois pendant la génération du projet, pas uniquement à la fin.

---

## Contraintes de sécurité obligatoires

Ce projet est un outil de purple team défensif et local. Il ne doit pas fournir de capacités offensives dangereuses.

Interdictions strictes :

- pas de malware ;
- pas de reverse shell ;
- pas de vol d'identifiants ;
- pas de credential dumping ;
- pas de contournement antivirus/EDR ;
- pas d'exploitation de vulnérabilités réelles ;
- pas de scan réseau agressif ;
- pas d'attaque contre des systèmes tiers ;
- pas de persistance réelle ;
- pas de chiffrement destructeur ;
- pas de suppression de logs système ;
- pas de mouvement latéral réel ;
- pas de payload dangereux ;
- pas d'instructions permettant d'attaquer une cible réelle.

Le simulateur doit fonctionner en priorité en mode synthétique : il génère des logs réalistes sans exécuter d'attaque réelle.

Un mode local optionnel peut exister, mais il doit être strictement bénin :

- uniquement dans un dossier `lab_sandbox/` ;
- uniquement avec des fichiers temporaires factices ;
- aucune élévation de privilèges ;
- aucune modification système dangereuse ;
- aucune connexion à une cible externe ;
- aucune action persistante ;
- nettoyage possible avec une commande `clean`.

Ajoute un fichier :

```text
SAFETY.md
```

Ce fichier doit expliquer clairement les limites de sécurité, le périmètre autorisé et les choix défensifs du projet.

---

## Vision produit

Le projet doit ressembler à un outil interne qu'une équipe SOC, blue team ou purple team pourrait utiliser pour tester sa couverture de détection.

Le workflow cible :

1. L'utilisateur liste les scénarios disponibles.
2. Il exécute un scénario de simulation.
3. Le système génère des logs réalistes au format JSONL.
4. Le moteur de détection applique des règles YAML.
5. Le système indique si les événements attendus ont été détectés.
6. Le dashboard affiche les scénarios, les alertes, la couverture MITRE ATT&CK et les résultats.
7. L'utilisateur exporte un rapport HTML, Markdown ou JSON.

Exemple d'utilisation CLI attendu :

```bash
pts list-scenarios
pts run suspicious-powershell
pts run-all
pts validate --run-id latest
pts report --run-id latest --format html
pts clean
```

L'acronyme CLI peut être `pts` pour `Purple Team Simulator`.

---

## Stack technique attendue

Backend :

- Python 3.11 ou supérieur ;
- FastAPI ;
- Pydantic ;
- SQLAlchemy ;
- SQLite par défaut ;
- Typer pour la CLI ;
- PyYAML pour scénarios et règles ;
- Jinja2 pour les rapports HTML/Markdown ;
- Pytest pour les tests.

Frontend :

- React ;
- TypeScript ;
- Vite ;
- interface claire, sobre et professionnelle ;
- dashboard responsive ;
- composants simples sans complexité inutile.

DevOps :

- Docker ;
- Docker Compose ;
- Makefile ;
- GitHub Actions CI ;
- `.env.example` ;
- `.gitignore` ;
- README professionnel.

Base de données :

- SQLite pour simplicité locale ;
- tables pour scénarios, runs, logs, alertes, détections, rapports.

---

## Architecture attendue

Structure minimale du dépôt :

```text
purple-team-attack-simulator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── scenario.py
│   │   │   ├── run.py
│   │   │   ├── log_event.py
│   │   │   ├── detection.py
│   │   │   └── alert.py
│   │   ├── schemas/
│   │   │   ├── scenario.py
│   │   │   ├── run.py
│   │   │   ├── log_event.py
│   │   │   ├── detection.py
│   │   │   └── report.py
│   │   ├── api/
│   │   │   ├── routes_scenarios.py
│   │   │   ├── routes_runs.py
│   │   │   ├── routes_detections.py
│   │   │   ├── routes_reports.py
│   │   │   └── routes_health.py
│   │   ├── services/
│   │   │   ├── scenario_loader.py
│   │   │   ├── scenario_runner.py
│   │   │   ├── synthetic_log_generator.py
│   │   │   ├── detection_engine.py
│   │   │   ├── mitre_mapper.py
│   │   │   ├── report_generator.py
│   │   │   └── coverage_calculator.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   └── main.py
│   │   └── utils/
│   │       ├── time.py
│   │       ├── jsonl.py
│   │       └── validators.py
│   ├── scenarios/
│   │   ├── suspicious_powershell.yml
│   │   ├── ssh_bruteforce.yml
│   │   ├── new_admin_user.yml
│   │   ├── scheduled_task_creation.yml
│   │   ├── temp_process_execution.yml
│   │   ├── suspicious_curl_download.yml
│   │   ├── process_masquerading.yml
│   │   ├── abnormal_login_time.yml
│   │   ├── webshell_like_request.yml
│   │   └── dns_exfil_pattern.yml
│   ├── rules/
│   │   ├── suspicious_powershell_rule.yml
│   │   ├── ssh_bruteforce_rule.yml
│   │   ├── new_admin_user_rule.yml
│   │   ├── scheduled_task_rule.yml
│   │   ├── temp_process_rule.yml
│   │   ├── suspicious_curl_rule.yml
│   │   ├── process_masquerading_rule.yml
│   │   ├── abnormal_login_time_rule.yml
│   │   ├── webshell_like_request_rule.yml
│   │   └── dns_exfil_pattern_rule.yml
│   ├── reports/
│   │   └── templates/
│   │       ├── report.html.j2
│   │       └── report.md.j2
│   ├── sample_data/
│   │   ├── sample_logs.jsonl
│   │   └── demo_run.json
│   ├── tests/
│   │   ├── test_scenario_loader.py
│   │   ├── test_scenario_runner.py
│   │   ├── test_detection_engine.py
│   │   ├── test_report_generator.py
│   │   └── test_api.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── StatCard.tsx
│   │   │   ├── ScenarioTable.tsx
│   │   │   ├── RunsTable.tsx
│   │   │   ├── AlertsTable.tsx
│   │   │   ├── CoverageMatrix.tsx
│   │   │   └── Timeline.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Scenarios.tsx
│   │   │   ├── Runs.tsx
│   │   │   ├── RunDetails.tsx
│   │   │   └── Reports.tsx
│   │   ├── types/
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docs/
│   ├── architecture.md
│   ├── demo_scenario.md
│   ├── detection_logic.md
│   ├── scenarios_catalog.md
│   ├── api_reference.md
│   ├── mitre_mapping.md
│   └── screenshots.md
├── lab_sandbox/
│   └── .gitkeep
├── generated_reports/
│   └── .gitkeep
├── generated_logs/
│   └── .gitkeep
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── Makefile
├── README.md
├── SAFETY.md
├── SUIVI_PROJET.md
├── LICENSE
├── .env.example
└── .gitignore
```

Si certains fichiers doivent être adaptés pour des raisons techniques, fais-le proprement, mais conserve cette architecture globale.

---

## Fonctionnalités backend obligatoires

### 1. API FastAPI

Créer une API REST avec les endpoints suivants :

```text
GET  /health
GET  /api/scenarios
GET  /api/scenarios/{scenario_id}
POST /api/scenarios/{scenario_id}/run
POST /api/runs/run-all
GET  /api/runs
GET  /api/runs/{run_id}
GET  /api/runs/{run_id}/logs
GET  /api/runs/{run_id}/alerts
POST /api/runs/{run_id}/validate
GET  /api/coverage
GET  /api/reports/{run_id}?format=html
GET  /api/reports/{run_id}?format=md
GET  /api/reports/{run_id}?format=json
```

L'API doit retourner des erreurs propres avec des statuts HTTP cohérents.

Ajouter une documentation OpenAPI automatique via FastAPI.

### 2. Base de données

Créer les modèles SQLAlchemy suivants :

#### Scenario

Champs :

- id ;
- name ;
- description ;
- platform ;
- tactic ;
- technique_id ;
- technique_name ;
- severity ;
- enabled ;
- created_at.

#### SimulationRun

Champs :

- id ;
- scenario_id ;
- status ;
- started_at ;
- finished_at ;
- mode ;
- result_summary.

#### LogEvent

Champs :

- id ;
- run_id ;
- timestamp ;
- source ;
- host ;
- user ;
- event_type ;
- event_id ;
- process_name ;
- command_line ;
- src_ip ;
- dst_ip ;
- raw_message ;
- event_json.

#### DetectionRule

Champs :

- id ;
- name ;
- description ;
- severity ;
- tactic ;
- technique_id ;
- enabled.

#### Alert

Champs :

- id ;
- run_id ;
- rule_id ;
- timestamp ;
- title ;
- severity ;
- matched_event_id ;
- reason ;
- mitre_technique_id ;
- mitre_tactic.

### 3. Chargement des scénarios YAML

Les scénarios doivent être définis en YAML.

Exemple de format :

```yaml
id: suspicious-powershell
name: Suspicious PowerShell Execution
description: Simulates suspicious PowerShell command-line activity using synthetic Windows process logs.
platform: windows
mode: synthetic
severity: high
mitre:
  tactic: Execution
  technique_id: T1059.001
  technique_name: PowerShell
expected_detection: suspicious_powershell_rule
log_profile:
  source: windows_security
  event_type: process_creation
  event_id: 4688
  host: WIN-LAB-01
  user: lab.user
simulation:
  generate_events: 6
  suspicious_events: 1
  safe: true
```

Le projet doit charger les fichiers depuis `backend/scenarios/`.

### 4. Chargement des règles YAML

Les règles de détection doivent être définies en YAML.

Exemple de format :

```yaml
id: suspicious_powershell_rule
name: Suspicious PowerShell Encoded Command Pattern
description: Detects synthetic PowerShell command lines containing suspicious encoded command indicators.
severity: high
mitre:
  tactic: Execution
  technique_id: T1059.001
  technique_name: PowerShell
logsource:
  source: windows_security
  event_type: process_creation
detection:
  condition: any
  fields:
    process_name:
      contains:
        - powershell
        - pwsh
    command_line:
      contains:
        - "-enc"
        - "EncodedCommand"
        - "FromBase64String"
false_positives:
  - Administrative scripts
  - Security testing tools
recommendation: Review the parent process, user context and script origin. Enforce PowerShell logging and constrained language mode where appropriate.
```

Le moteur de détection doit supporter au minimum :

- `equals` ;
- `contains` ;
- `regex` ;
- `not_contains` ;
- conditions `all` et `any` ;
- matching sur plusieurs champs ;
- sévérité ;
- mapping MITRE.

### 5. Moteur de simulation

Créer un moteur qui exécute un scénario en mode synthétique.

Il doit :

- créer un `SimulationRun` ;
- générer des événements JSON réalistes ;
- stocker les événements en base ;
- écrire les événements dans `generated_logs/<run_id>.jsonl` ;
- appliquer automatiquement les règles de détection ;
- créer des alertes si des règles matchent ;
- produire un résumé de résultat.

Le moteur doit générer des logs réalistes mais sans danger.

Exemple d'événement JSONL :

```json
{
  "timestamp": "2026-01-01T10:15:30Z",
  "source": "windows_security",
  "host": "WIN-LAB-01",
  "user": "lab.user",
  "event_type": "process_creation",
  "event_id": 4688,
  "process_name": "powershell.exe",
  "command_line": "powershell.exe -NoProfile -EncodedCommand <synthetic-demo-value>",
  "src_ip": null,
  "dst_ip": null,
  "raw_message": "Synthetic process creation event for detection testing"
}
```

### 6. Scénarios obligatoires

Créer au minimum 10 scénarios.

#### Scénario 1 — Suspicious PowerShell

- ID : `suspicious-powershell`
- Plateforme : Windows
- MITRE : T1059.001
- Tactique : Execution
- Type de logs : process creation
- Danger : aucun, logs synthétiques uniquement

#### Scénario 2 — SSH Brute Force Pattern

- ID : `ssh-bruteforce`
- Plateforme : Linux
- MITRE : T1110
- Tactique : Credential Access
- Type de logs : auth logs synthétiques
- Générer plusieurs échecs de connexion depuis la même IP

#### Scénario 3 — New Admin User Created

- ID : `new-admin-user`
- Plateforme : Windows/Linux générique
- MITRE : T1136
- Tactique : Persistence
- Type de logs : user management
- Générer un événement de création d'utilisateur admin fictif

#### Scénario 4 — Scheduled Task Creation

- ID : `scheduled-task-creation`
- Plateforme : Windows
- MITRE : T1053
- Tactique : Execution / Persistence
- Type de logs : scheduled task synthetic logs

#### Scénario 5 — Process Execution from Temp Directory

- ID : `temp-process-execution`
- Plateforme : Windows
- MITRE : T1204 ou T1059 selon choix cohérent
- Tactique : Execution
- Type de logs : process creation

#### Scénario 6 — Suspicious Curl Download

- ID : `suspicious-curl-download`
- Plateforme : Linux
- MITRE : T1105
- Tactique : Command and Control
- Type de logs : process/network synthetic logs
- Ne pas télécharger réellement de fichier

#### Scénario 7 — Process Masquerading

- ID : `process-masquerading`
- Plateforme : Windows/Linux
- MITRE : T1036
- Tactique : Defense Evasion
- Type de logs : process creation
- Utiliser uniquement logs synthétiques

#### Scénario 8 — Abnormal Login Time

- ID : `abnormal-login-time`
- Plateforme : Identity / IAM générique
- MITRE : T1078
- Tactique : Defense Evasion / Initial Access
- Type de logs : authentication
- Simuler une connexion hors horaires habituels

#### Scénario 9 — Webshell-like HTTP Request

- ID : `webshell-like-request`
- Plateforme : Web
- MITRE : T1505.003
- Tactique : Persistence
- Type de logs : web access logs synthétiques
- Ne pas fournir de webshell réel

#### Scénario 10 — DNS Exfiltration Pattern

- ID : `dns-exfil-pattern`
- Plateforme : Network
- MITRE : T1048 ou T1071.004 selon choix cohérent
- Tactique : Exfiltration / Command and Control
- Type de logs : DNS synthétiques
- Ne faire aucune exfiltration réelle

Chaque scénario doit avoir :

- un fichier YAML ;
- une règle de détection YAML ;
- des logs synthétiques générés ;
- un test unitaire prouvant que la règle détecte le scénario ;
- une entrée dans la documentation `docs/scenarios_catalog.md` ;
- une entrée dans `docs/mitre_mapping.md`.

### 7. Moteur de validation

Créer une fonction de validation qui compare :

- détection attendue ;
- détection obtenue ;
- nombre d'alertes ;
- sévérité ;
- mapping MITRE.

Résultat attendu :

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

### 8. Couverture MITRE

Créer un service `coverage_calculator.py` qui calcule :

- nombre de scénarios ;
- nombre de techniques MITRE couvertes ;
- nombre de tactiques couvertes ;
- scénarios détectés ;
- scénarios non détectés ;
- taux de couverture ;
- alertes par sévérité.

---

## Fonctionnalités CLI obligatoires

Créer une CLI avec Typer.

Commande principale :

```bash
pts
```

Commandes obligatoires :

```bash
pts list-scenarios
pts show-scenario <scenario_id>
pts run <scenario_id>
pts run-all
pts validate <run_id>
pts validate latest
pts coverage
pts report <run_id> --format html
pts report <run_id> --format md
pts report <run_id> --format json
pts clean
pts serve-api
```

La CLI doit afficher des sorties lisibles.

Exemple :

```text
Scenario executed successfully
Run ID: 20260101-101530-suspicious-powershell
Generated logs: generated_logs/20260101-101530-suspicious-powershell.jsonl
Alerts: 1
Coverage: covered
```

Prévoir une installation locale simple :

```bash
cd backend
pip install -e .
pts list-scenarios
```

---

## Fonctionnalités frontend obligatoires

Créer un dashboard web professionnel.

Pages minimales :

### Dashboard

Afficher :

- nombre total de scénarios ;
- nombre total de runs ;
- nombre total d'alertes ;
- taux de couverture ;
- alertes par sévérité ;
- dernières simulations ;
- top techniques MITRE.

### Scenarios

Table avec :

- nom ;
- description ;
- plateforme ;
- tactique ;
- technique MITRE ;
- sévérité ;
- bouton `Run`.

### Runs

Table avec :

- run id ;
- scénario ;
- statut ;
- date ;
- nombre de logs ;
- nombre d'alertes ;
- résultat de validation.

### Run Details

Afficher :

- détails du scénario ;
- timeline des logs ;
- alertes générées ;
- règle matchée ;
- mapping MITRE ;
- bouton export rapport.

### Reports

Afficher :

- liste des rapports générés ;
- liens vers export HTML/Markdown/JSON.

### Coverage Matrix

Afficher une matrice simple :

```text
Technique MITRE | Tactique | Scénario | Détection attendue | Statut
```

Statuts possibles :

- `covered` ;
- `not_detected` ;
- `not_tested`.

---

## Rapports obligatoires

Le projet doit générer des rapports en :

- HTML ;
- Markdown ;
- JSON.

Emplacement :

```text
generated_reports/
```

Contenu d'un rapport :

```markdown
# Purple Team Simulation Report

## Executive Summary

Résumé clair du scénario, de l'objectif et du résultat.

## Scenario Details

- Scenario ID:
- Name:
- Platform:
- MITRE Tactic:
- MITRE Technique:
- Severity:

## Simulation Result

- Run ID:
- Start time:
- End time:
- Generated logs:
- Alerts generated:
- Detection status:

## Detection Logic

Règle utilisée, champs matchés, raison de l'alerte.

## Timeline

Table chronologique des principaux événements.

## Alerts

Table des alertes générées.

## Defensive Recommendations

Recommandations SOC concrètes.

## Limitations

Rappel : simulation synthétique, aucun comportement offensif réel.
```

Le rapport HTML doit être lisible et professionnel sans dépendance externe complexe.

---

## Documentation obligatoire

Créer un README très professionnel.

Le README doit contenir :

1. titre du projet ;
2. badges GitHub Actions si possible ;
3. résumé clair ;
4. problème résolu ;
5. fonctionnalités ;
6. architecture ;
7. stack ;
8. installation locale ;
9. lancement avec Docker ;
10. utilisation CLI ;
11. utilisation API ;
12. utilisation dashboard ;
13. exemples de scénarios ;
14. exemple de rapport ;
15. mapping MITRE ;
16. sécurité et limites ;
17. tests ;
18. roadmap ;
19. screenshots à ajouter ;
20. licence.

Créer aussi :

### docs/architecture.md

Décrire :

- architecture globale ;
- flux de données ;
- choix backend ;
- choix frontend ;
- choix base de données ;
- séparation scénarios/règles/moteur.

### docs/demo_scenario.md

Créer un scénario de démonstration complet :

```bash
make setup
make demo
make report
```

Expliquer ce que l'utilisateur doit voir.

### docs/detection_logic.md

Expliquer :

- format des règles ;
- conditions `all` et `any` ;
- matchers ;
- faux positifs ;
- recommandations.

### docs/scenarios_catalog.md

Lister les 10 scénarios avec :

- ID ;
- description ;
- source de logs ;
- MITRE ;
- règle associée ;
- résultat attendu.

### docs/mitre_mapping.md

Créer une table :

```text
Scenario | Tactic | Technique ID | Technique Name | Detection Rule | Severity
```

### docs/api_reference.md

Documenter les endpoints principaux.

### SAFETY.md

Expliquer les limites de sécurité et l'usage autorisé.

---

## Tests obligatoires

Ajouter des tests Pytest.

Tests minimum :

- chargement des scénarios YAML ;
- chargement des règles YAML ;
- génération de logs synthétiques ;
- détection positive pour chaque scénario ;
- absence de détection sur logs bénins ;
- génération de rapport ;
- endpoints API principaux ;
- calcul de couverture.

Objectif : au moins 20 tests.

Tous les tests doivent passer avec :

```bash
make test
```

---

## Makefile obligatoire

Créer un Makefile avec :

```makefile
setup
install-backend
install-frontend
run-api
run-frontend
run-cli-demo
demo
test
lint
format
clean
docker-build
docker-up
docker-down
report
```

La commande :

```bash
make demo
```

Doit :

1. lancer une ou plusieurs simulations ;
2. générer des logs ;
3. appliquer les règles ;
4. créer des alertes ;
5. générer un rapport ;
6. afficher le chemin du rapport.

---

## Docker obligatoire

Créer un `docker-compose.yml` permettant de lancer :

- backend FastAPI ;
- frontend React ;
- volume pour `generated_logs/` ;
- volume pour `generated_reports/`.

Commandes attendues :

```bash
docker compose up --build
```

Endpoints attendus :

```text
Backend:  http://localhost:8000
Frontend: http://localhost:5173
API docs: http://localhost:8000/docs
```

---

## CI GitHub Actions obligatoire

Créer `.github/workflows/ci.yml`.

La CI doit :

- installer Python ;
- installer les dépendances backend ;
- exécuter les tests Pytest ;
- installer Node ;
- installer les dépendances frontend ;
- lancer le build frontend ;
- échouer si les tests ou le build échouent.

---

## Exigences de qualité

Le code doit être :

- clair ;
- modulaire ;
- typé autant que possible ;
- commenté quand nécessaire ;
- maintenable ;
- sans complexité inutile ;
- compatible Linux/macOS/Windows autant que possible.

Ne pas faire un simple prototype non structuré.

Le projet doit donner l'impression d'un vrai outil interne de cybersécurité.

---

## Données de démonstration

Créer des données de démonstration réalistes.

Inclure :

- logs Windows synthétiques ;
- logs Linux SSH synthétiques ;
- logs web synthétiques ;
- logs DNS synthétiques ;
- logs IAM/authentication synthétiques.

Les logs doivent être stockés au format JSONL.

Chaque ligne doit être un JSON valide.

---

## Exemple de scénario utilisateur attendu

Après génération du projet, l'utilisateur doit pouvoir faire :

```bash
git clone <repo>
cd purple-team-attack-simulator
make setup
make demo
```

Puis voir :

```text
Running scenario: suspicious-powershell
Generated events: 6
Applied detection rules: 10
Alerts generated: 1
Coverage status: covered
Report generated: generated_reports/latest_report.html
```

Puis lancer :

```bash
make docker-up
```

Et accéder à :

```text
http://localhost:5173
```

---

## Critères d'acceptation finaux

Le projet est terminé uniquement si :

- le backend démarre ;
- le frontend démarre ;
- la CLI fonctionne ;
- les 10 scénarios existent ;
- les 10 règles existent ;
- chaque scénario génère des logs ;
- chaque règle détecte son scénario ;
- les rapports HTML, Markdown et JSON sont générés ;
- `make demo` fonctionne ;
- `make test` fonctionne ;
- `docker compose up --build` fonctionne ;
- le README est complet ;
- `SUIVI_PROJET.md` est complet et mis à jour ;
- `SAFETY.md` existe ;
- aucune fonctionnalité offensive dangereuse n'est présente.

---

## Contenu attendu du README

Le README doit être particulièrement soigné, car il sera affiché sur GitHub et lu par un recruteur.

Il doit inclure ce type de phrase :

```markdown
Purple Team Attack Simulator is a local defensive cybersecurity lab designed to emulate controlled adversary-like behaviors through synthetic logs, validate detection rules, map results to MITRE ATT&CK, and generate SOC-ready reports.
```

Ajouter une section :

```markdown
## Why this project matters

Security teams need a safe way to validate whether their detection logic works before a real incident occurs. This project provides a controlled local environment to simulate attacker-like patterns, generate telemetry, validate detections, and report coverage gaps.
```

Ajouter une section :

```markdown
## Safety-first design

This tool does not exploit systems, steal credentials, deploy malware, bypass security tools, or perform destructive actions. It generates synthetic telemetry for authorized defensive testing and education.
```

---

## Roadmap à inclure

Dans le README, ajouter une roadmap :

- ajout de nouveaux scénarios ;
- export Sigma ;
- intégration Elastic/Splunk/Sentinel ;
- import de logs réels autorisés ;
- matrice ATT&CK plus visuelle ;
- scoring de maturité SOC ;
- mode multi-environnement ;
- authentification optionnelle pour dashboard.

---

## Style visuel frontend

Le frontend doit être sobre et professionnel.

Préférences :

- fond clair ;
- cartes de statistiques ;
- tables propres ;
- badges de sévérité ;
- timeline lisible ;
- pas d'animations inutiles ;
- pas de design trop fantaisie.

Couleurs possibles :

- gris foncé ;
- bleu ;
- violet léger ;
- rouge/orange pour criticité.

---

## Consigne importante pour l'agent

Ne te contente pas de créer des fichiers vides ou des TODO.

Tu dois implémenter réellement :

- la logique backend ;
- les scénarios ;
- les règles ;
- la génération de logs ;
- le moteur de détection ;
- la CLI ;
- les rapports ;
- les tests ;
- le frontend ;
- Docker ;
- la documentation.

Les TODO sont acceptés uniquement dans la roadmap, pas dans le code principal.

Si une fonctionnalité est trop complexe, implémente une version simple mais fonctionnelle.

Priorité : projet complet, cohérent, exécutable et professionnel.

---

## Ordre recommandé de construction

Suis cet ordre :

1. Créer l'arborescence complète.
2. Créer `SUIVI_PROJET.md` et écrire l'étape 1.
3. Créer backend minimal FastAPI.
4. Créer modèles SQLAlchemy et base SQLite.
5. Créer chargeur de scénarios YAML.
6. Créer chargeur de règles YAML.
7. Créer moteur de génération de logs synthétiques.
8. Créer moteur de détection.
9. Créer 10 scénarios YAML.
10. Créer 10 règles YAML.
11. Créer CLI Typer.
12. Créer endpoints API.
13. Créer génération de rapports.
14. Créer tests Pytest.
15. Créer frontend React.
16. Créer Dockerfiles et docker-compose.
17. Créer Makefile.
18. Créer GitHub Actions.
19. Créer documentation complète.
20. Mettre à jour `SUIVI_PROJET.md` avec le bilan final.
21. Vérifier que les commandes principales fonctionnent.

À chaque étape importante, mets à jour `SUIVI_PROJET.md`.

---

## Commandes finales à vérifier

À la fin, vérifie ou fournis clairement les commandes :

```bash
make setup
make test
make demo
make docker-up
```

Et aussi :

```bash
cd backend
pip install -e .
pts list-scenarios
pts run suspicious-powershell
pts report latest --format html
```

---

## Résultat final attendu

À la fin de ton travail, le dépôt doit être prêt à être poussé sur GitHub.

Le projet doit être suffisamment sérieux pour être présenté dans un CV ou en entretien pour des postes comme :

- SOC Analyst junior ;
- Blue Team junior ;
- Detection Engineer junior ;
- Cybersecurity Engineer junior ;
- DevSecOps junior ;
- Purple Team junior.

Le projet doit montrer :

- compréhension des scénarios d'attaque ;
- approche défensive ;
- mapping MITRE ATT&CK ;
- génération de logs ;
- détection ;
- reporting ;
- API ;
- CLI ;
- dashboard ;
- Docker ;
- tests ;
- documentation professionnelle.

---

## Dernière consigne

Commence maintenant la création du projet complet dans le répertoire courant.

Ne demande pas de clarification sauf blocage technique majeur.

Fais des choix raisonnables si nécessaire.

Maintiens `SUIVI_PROJET.md` à jour pendant toute la génération.
