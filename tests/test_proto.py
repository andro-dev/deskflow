"""Clickable Tekforce prototype: HTML loop, sample data only."""

from __future__ import annotations

from fastapi.testclient import TestClient

from deskflow.proto import store


def test_home_is_tekforce_two_doors(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    body = response.text
    assert "Tekforce" in body
    assert "Hire talent" in body
    assert "Find work" in body
    assert "Walk the loop" in body


def test_job_board_lists_public_sample_role(client: TestClient) -> None:
    response = client.get("/jobs")
    assert response.status_code == 200
    assert "Senior Python SDET" in response.text
    assert "Controller" not in response.text


def test_pending_job_is_not_on_public_detail(client: TestClient) -> None:
    response = client.get("/jobs/controller", follow_redirects=False)
    assert response.status_code == 303


def test_view_as_sets_cookie(client: TestClient) -> None:
    response = client.post(
        "/view",
        data={"as": "recruiter", "next": "/desk/approve"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/desk/approve"
    assert response.cookies.get("tekforce_view") == "recruiter"


def test_full_loop_draft_approve_apply_slate(client: TestClient) -> None:
    drafted = client.post(
        "/hire",
        data={
            "title": "Revenue Cycle Manager",
            "vertical": "Medical",
            "placement_type": "Contract-to-hire",
            "description": "Fictional hire request.",
        },
        follow_redirects=True,
    )
    assert drafted.status_code == 200
    assert "waiting for Tekforce approval" in drafted.text

    pending = client.get("/desk/approve")
    assert "Revenue Cycle Manager" in pending.text

    approved = client.post("/desk/approve/controller", follow_redirects=True)
    assert approved.status_code == 200
    assert "Controller" in approved.text
    assert "Find work" in approved.text

    applied = client.post(
        "/jobs/sdet/apply",
        data={"name": "Alex Rivera", "headline": "Senior test engineer, Python automation"},
        follow_redirects=True,
    )
    assert applied.status_code == 200
    assert "My applications" in applied.text
    assert "Senior Python SDET" in applied.text

    slate = client.post(
        "/desk/jobs/sdet/slate",
        data={"application_id": "app-alex-sdet"},
        follow_redirects=True,
    )
    assert slate.status_code == 200
    assert "Slate sent" in slate.text

    client_view = client.get("/me/jobs/sdet")
    assert "Alex Rivera" in client_view.text
    assert "86" in client_view.text


def test_header_has_my_tekforce_link(client: TestClient) -> None:
    response = client.get("/")
    assert "My Tekforce" in response.text
    assert "/my-tekforce/login" in response.text


def test_my_tekforce_login_page(client: TestClient) -> None:
    response = client.get("/my-tekforce/login")
    assert response.status_code == 200
    body = response.text
    assert "Log in" in body
    assert "alex.rivera@example.com" in body
    assert "Register" in body
    assert "Forgot password" in body


def test_login_sample_candidate_sets_cookie(client: TestClient) -> None:
    response = client.post(
        "/my-tekforce/login",
        data={"email": "alex.rivera@example.com", "password": "anything"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"].startswith("/applications")
    assert response.cookies.get("tekforce_view") == "candidate"


def test_unknown_email_stays_on_login(client: TestClient) -> None:
    response = client.post(
        "/my-tekforce/login",
        data={"email": "not-a-sample@example.com", "password": "x"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Use a sample account" in response.text


def test_my_tekforce_hub_after_login(client: TestClient) -> None:
    client.post(
        "/my-tekforce/login",
        data={"email": "morgan.hale@lumenfield.example", "password": "sample"},
    )
    hub = client.get("/my-tekforce")
    assert hub.status_code == 200
    assert "Signed in" in hub.text
    assert "My jobs" in hub.text


def test_evaluate_api_still_separate(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_store_reset_restores_seed() -> None:
    store.draft_job("Temp", "IT", "Permanent", "x")
    assert any(job["title"] == "Temp" for job in store.jobs())
    store.reset()
    assert not any(job["title"] == "Temp" for job in store.jobs())
    assert store.job_by_id("sdet") is not None
