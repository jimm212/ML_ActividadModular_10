import client
import json
import pytest
from app import app

BASE = "http://127.0.0.1:5000"

@pytest.fixture
def client():
    return app.test_client()


def test_health(client):
    r = client.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_model_info(client):
    r = client.get(f"{BASE}/model-info")
    assert r.status_code == 200
    assert "model_name" in r.json()

def test_predict_valid(client):
    with open("tests/sample_valid.json") as f:
        payload = json.load(f)
    r = client.post(f"{BASE}/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "probability" in data

def test_predict_invalid(client):
    payload = {"wrong": "data"}
    r = client.post(f"{BASE}/predict", json=payload)
    assert r.status_code == 500 or r.status_code == 400
    assert "error" in r.json()
