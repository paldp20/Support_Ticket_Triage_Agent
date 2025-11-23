# some edge cases

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_basic_triage():
    response = client.post("/triage", json={"description": "Fever and cough"})
    assert response.status_code == 200
    data = response.json()

    # check new response schema
    assert "summary" in data
    assert "category" in data
    assert "best_kb_match" in data
    assert "recommended_action" in data["best_kb_match"]
    assert "kb_matches" in data

def test_empty_input():
    response = client.post("/triage", json={"description": ""})
    # API rejects empty text -> correct expected status:
    assert response.status_code == 400

def test_long_input():
    long_text = "fever " * 5000
    response = client.post("/triage", json={"description": long_text})
    assert response.status_code == 200
    data = response.json()

    assert "summary" in data
    assert "best_kb_match" in data

def test_special_characters():
    weird = "@@@@####!!! ??? /// &&&"
    response = client.post("/triage", json={"description": weird})
    assert response.status_code == 200
    data = response.json()

    assert "summary" in data
    assert "best_kb_match" in data

def test_no_json_body():
    response = client.post("/triage")
    assert response.status_code == 422