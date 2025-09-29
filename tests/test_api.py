import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json().get("status") == "ok"

def test_model_info(client):
    r = client.get("/model-info")
    assert r.status_code == 200
    assert "model_name" in r.get_json()

def test_predict_valid(client):
    with open("tests/sample_valid.json") as f:
        payload = json.load(f)
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert "prediction" in data
    assert "probability" in data

def test_predict_invalid(client):
    payload = {"wrong": "data"}
    r = client.post("/predict", json=payload)
    assert r.status_code in (400, 500)
    assert "error" in r.get_json()

