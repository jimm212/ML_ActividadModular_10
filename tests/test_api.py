import requests
import json

BASE = "http://127.0.0.1:5000"

def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_model_info():
    r = requests.get(f"{BASE}/model-info")
    assert r.status_code == 200
    assert "model_name" in r.json()

def test_predict_valid():
    with open("tests/sample_valid.json") as f:
        payload = json.load(f)
    r = requests.post(f"{BASE}/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "probability" in data

def test_predict_invalid():
    payload = {"wrong": "data"}
    r = requests.post(f"{BASE}/predict", json=payload)
    assert r.status_code == 500 or r.status_code == 400
    assert "error" in r.json()
