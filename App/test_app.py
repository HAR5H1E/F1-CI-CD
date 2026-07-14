from fastapi.testclient import TestClient
from app import app

Tclient = TestClient(app=app)

def test_Health():
    response = Tclient.get("/health")

    assert response.status_code == 200
    assert response.json() == {"Status": "Ok"}

def test_Predict():
    payload = {
        "Abbreviation": "LEC",
        "TeamName": "Ferrari",
        "CountryEvent": "Bahrain Grand Prix",
        "GridPosition": 2.0,
        "GapPole": 0.100,
        "GapLeaderFP": 0.300
        }
    response = Tclient.post("/Predict",json=payload)

    assert response.status_code == 200
    assert "Final" in response.json()

def test_PreditFail():
    payload = {
        "Abbreviation": "LEC",
        "TeamName": "Ferrari",
        "CountryEvent": "Bahrain Grand Prix",
        }
    response = Tclient.post("/Predict",json=payload)

    assert response.status_code == 422

def test_Web():
    response = Tclient.get("/")

    assert response.status_code == 200

