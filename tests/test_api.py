"""API tests — the SDET artifact for Deskflow.

These tests treat the HTTP surface as the product: status codes, schema, and
observable scoring behavior. They run without paid API keys.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_ok_without_llm_key(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"]
    assert body["llm_configured"] is False


def test_samples_endpoint_points_at_fictional_files(client: TestClient) -> None:
    response = client.get("/v1/samples")
    assert response.status_code == 200
    body = response.json()
    assert "Sample data only" in body["notice"]
    assert "strong_fit_sdet.json" in body["files"]
    assert "weak_fit_manual_qa.json" in body["files"]


def test_evaluate_rejects_empty_body(client: TestClient) -> None:
    response = client.post("/v1/evaluate", json={})
    assert response.status_code == 422


def test_evaluate_rejects_missing_job_description(client: TestClient) -> None:
    response = client.post(
        "/v1/evaluate",
        json={
            "job": {"title": "SDET"},
            "candidate": {"name": "Alex Rivera"},
        },
    )
    assert response.status_code == 422


def test_evaluate_strong_sample_returns_score_evidence_and_note(
    client: TestClient, strong_payload: dict
) -> None:
    response = client.post("/v1/evaluate", json=strong_payload)
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["fit_score"] <= 100
    assert body["fit_score"] >= 75
    assert body["recommendation"] == "strong_fit"
    assert body["scorer"] == "heuristic"
    assert body["evidence"]
    assert any(item["kind"] == "match" for item in body["evidence"])
    assert "Alex" in body["draft_note"]
    assert "Lumenfield Labs" in body["draft_note"]
    assert body["extracted_job"]["required_skills"]
    assert "python" in body["extracted_candidate"]["skills"]
    assert "pytest" in body["extracted_candidate"]["skills"]


def test_evaluate_weak_sample_scores_below_strong(
    client: TestClient, strong_payload: dict, weak_payload: dict
) -> None:
    strong = client.post("/v1/evaluate", json=strong_payload).json()
    weak = client.post("/v1/evaluate", json=weak_payload).json()
    assert weak["fit_score"] < strong["fit_score"]
    assert weak["fit_score"] < 50
    assert weak["recommendation"] == "weak_fit"
    assert any(item["kind"] == "gap" for item in weak["evidence"])
    assert "Screening note" in weak["draft_note"]


def test_evaluate_is_deterministic(client: TestClient, strong_payload: dict) -> None:
    first = client.post("/v1/evaluate", json=strong_payload).json()
    second = client.post("/v1/evaluate", json=strong_payload).json()
    assert first["fit_score"] == second["fit_score"]
    assert first["evidence"] == second["evidence"]
    assert first["draft_note"] == second["draft_note"]


def test_note_style_outreach_versus_screening(
    client: TestClient, strong_payload: dict
) -> None:
    outreach = dict(strong_payload)
    outreach["note_style"] = "outreach"
    screening = dict(strong_payload)
    screening["note_style"] = "screening"

    outreach_note = client.post("/v1/evaluate", json=outreach).json()["draft_note"]
    screening_note = client.post("/v1/evaluate", json=screening).json()["draft_note"]

    assert outreach_note.startswith("Subject:")
    assert screening_note.startswith("Screening note")
    assert outreach_note != screening_note


def test_openapi_documents_evaluate(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/v1/evaluate" in paths
    assert "/health" in paths
