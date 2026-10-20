from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

client = TestClient(app)
PROMPT = "Resume el siguiente artículo sobre inflación en Latinoamérica"


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_ok():
    response = client.post("/api/v1/prompts/analyze", json={"prompt": PROMPT})
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["score"] <= 100
    assert body["level"] in {"weak", "acceptable", "good"}
    assert len(body["checks"]) == 6


def test_refine_ok():
    response = client.post("/api/v1/prompts/refine", json={"prompt": PROMPT})
    assert response.status_code == 200
    assert response.json()["needs_completion"] is True


def test_blank_prompt_returns_standard_error():
    response = client.post("/api/v1/prompts/analyze", json={"prompt": "   "})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "validation_error"
    assert error["details"][0]["field"] == "prompt"


def test_missing_field_is_rejected():
    response = client.post("/api/v1/prompts/refine", json={})
    assert response.status_code == 422


def test_prompt_too_long_is_rejected():
    too_long = "a" * (get_settings().max_chars + 1)
    response = client.post("/api/v1/prompts/analyze", json={"prompt": too_long})
    assert response.status_code == 422


def test_unknown_route_uses_standard_error_format():
    response = client.get("/api/v1/nope")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "http_error"
