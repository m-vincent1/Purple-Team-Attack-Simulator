import pytest


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_scenarios(client):
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10


def test_get_scenario_by_id(client):
    response = client.get("/api/scenarios/suspicious-powershell")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "suspicious-powershell"
    assert data["technique_id"] == "T1059.001"


def test_get_scenario_not_found(client):
    response = client.get("/api/scenarios/nonexistent")
    assert response.status_code == 404


def test_run_scenario_endpoint(client):
    response = client.post("/api/scenarios/suspicious-powershell/run")
    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    assert data["events_generated"] > 0


def test_list_runs(client):
    # First run a scenario
    client.post("/api/scenarios/ssh-bruteforce/run")
    response = client.get("/api/runs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_coverage_endpoint(client):
    client.post("/api/scenarios/suspicious-powershell/run")
    response = client.get("/api/coverage")
    assert response.status_code == 200
    data = response.json()
    assert "total_scenarios" in data
    assert "coverage_rate" in data
    assert data["total_scenarios"] == 10


def test_validate_run(client):
    run_response = client.post("/api/scenarios/suspicious-powershell/run")
    run_id = run_response.json()["run_id"]
    response = client.post(f"/api/runs/{run_id}/validate")
    assert response.status_code == 200
    data = response.json()
    assert data["detected"] == True
    assert data["coverage_status"] == "covered"
