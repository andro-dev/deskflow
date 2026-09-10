"""In-memory sample data for the clickable prototype.

Names and companies are fictional. Restarting the process resets the loop.
"""

from __future__ import annotations

from copy import deepcopy
from itertools import count
from typing import Any

ROLES = ("visitor", "candidate", "client", "recruiter", "exec")

VERTICALS = (
    "IT",
    "CEO Search",
    "Medical",
    "Financial",
    "Legal",
    "Skilled trades",
)

PLACEMENT_TYPES = (
    "Contract",
    "Contract-to-hire",
    "Permanent",
    "Executive search",
)

HOME_AFTER_LOGIN: dict[str, str] = {
    "candidate": "/applications",
    "client": "/me/jobs",
    "recruiter": "/desk/jobs",
    "exec": "/desk/approve",
}

SAMPLE_ACCOUNTS: tuple[dict[str, str], ...] = (
    {
        "email": "alex.rivera@example.com",
        "name": "Alex Rivera",
        "role": "candidate",
        "label": "Candidate",
    },
    {
        "email": "morgan.hale@lumenfield.example",
        "name": "Morgan Hale",
        "role": "client",
        "label": "Client · Lumenfield Labs",
    },
    {
        "email": "sam.okonkwo@tekforce.example",
        "name": "Sam Okonkwo",
        "role": "recruiter",
        "label": "Recruiter",
    },
    {
        "email": "exec@tekforce.example",
        "name": "Exec",
        "role": "exec",
        "label": "Exec",
    },
)

NAV: dict[str, tuple[tuple[str, str], ...]] = {
    "visitor": (
        ("Find work", "/jobs"),
        ("Hire talent", "/hire"),
    ),
    "candidate": (
        ("Jobs", "/jobs"),
        ("My applications", "/applications"),
    ),
    "client": (
        ("Hire", "/hire"),
        ("My jobs", "/me/jobs"),
    ),
    "recruiter": (
        ("Jobs", "/jobs"),
        ("Approve", "/desk/approve"),
        ("Desk", "/desk/jobs"),
    ),
    "exec": (
        ("Jobs", "/jobs"),
        ("Approve", "/desk/approve"),
        ("Desk", "/desk/jobs"),
        ("Hire", "/hire"),
    ),
}

_id = count(100)

_SEED: dict[str, Any] = {
    "jobs": [
        {
            "id": "sdet",
            "title": "Senior Python SDET",
            "account": "Lumenfield Labs",
            "vertical": "IT",
            "placement_type": "Permanent",
            "location": "Remote",
            "status": "public",
            "summary": "Build and own API tests for internal Python services. Sample role only.",
            "description": (
                "Lumenfield Labs (fictional) is hiring a Senior Python SDET for internal "
                "developer tools.\n\nRequired: Python, pytest, API testing, FastAPI, "
                "GitHub Actions, Docker.\nNice to have: Playwright, AWS, SQL."
            ),
            "slate_sent": False,
            "slate_application_ids": [],
        },
        {
            "id": "controller",
            "title": "Controller",
            "account": "Lumenfield Labs",
            "vertical": "Financial",
            "placement_type": "Permanent",
            "location": "New York, NY",
            "status": "pending",
            "summary": "Own close, controls, and reporting for a small operating company.",
            "description": (
                "Client draft. Needs Tekforce approval before it appears on the public board. "
                "Fictional req for the prototype loop."
            ),
            "slate_sent": False,
            "slate_application_ids": [],
        },
    ],
    "applications": [
        {
            "id": "app-alex-sdet",
            "job_id": "sdet",
            "candidate_name": "Alex Rivera",
            "headline": "Senior test engineer, Python automation",
            "stage": "Screening",
            "fit_score": 86,
            "recommendation": "strong_fit",
            "owner": "candidate",
        },
        {
            "id": "app-jordan-sdet",
            "job_id": "sdet",
            "candidate_name": "Jordan Lee",
            "headline": "Manual QA, documentation",
            "stage": "Applied",
            "fit_score": 31,
            "recommendation": "weak_fit",
            "owner": "recruiter",
        },
    ],
}


_state: dict[str, Any] | None = None


def account_for_email(email: str) -> dict[str, str] | None:
    needle = email.strip().lower()
    return next((row for row in SAMPLE_ACCOUNTS if row["email"] == needle), None)


def my_tekforce_href(persona: str) -> str:
    if persona == "visitor":
        return "/my-tekforce/login"
    return "/my-tekforce"


def reset() -> None:
    global _state
    _state = deepcopy(_SEED)


def state() -> dict[str, Any]:
    if _state is None:
        reset()
    assert _state is not None
    return _state


def jobs() -> list[dict[str, Any]]:
    return state()["jobs"]


def job_by_id(job_id: str) -> dict[str, Any] | None:
    return next((job for job in jobs() if job["id"] == job_id), None)


def public_jobs() -> list[dict[str, Any]]:
    return [job for job in jobs() if job["status"] == "public"]


def pending_jobs() -> list[dict[str, Any]]:
    return [job for job in jobs() if job["status"] == "pending"]


def applications(job_id: str | None = None) -> list[dict[str, Any]]:
    rows = state()["applications"]
    if job_id is None:
        return rows
    return [row for row in rows if row["job_id"] == job_id]


def candidate_applications() -> list[dict[str, Any]]:
    """Applications the sample candidate can see (Alex + anything they submitted)."""
    rows = []
    for row in applications():
        if row["candidate_name"] == "Alex Rivera" or row.get("owner") == "candidate":
            job = job_by_id(row["job_id"])
            rows.append({**row, "job": job})
    return rows


def already_applied(job_id: str, name: str) -> bool:
    return any(
        row["job_id"] == job_id and row["candidate_name"] == name for row in applications()
    )


def apply(job_id: str, name: str, headline: str) -> dict[str, Any] | None:
    job = job_by_id(job_id)
    if job is None or job["status"] != "public":
        return None
    if already_applied(job_id, name):
        return next(
            row
            for row in applications()
            if row["job_id"] == job_id and row["candidate_name"] == name
        )
    row = {
        "id": f"app-{next(_id)}",
        "job_id": job_id,
        "candidate_name": name,
        "headline": headline or "Candidate",
        "stage": "Applied",
        "fit_score": None,
        "recommendation": None,
        "owner": "candidate",
    }
    state()["applications"].append(row)
    return row


def draft_job(
    title: str,
    vertical: str,
    placement_type: str,
    description: str,
    account: str = "Lumenfield Labs",
) -> dict[str, Any]:
    job = {
        "id": f"job-{next(_id)}",
        "title": title,
        "account": account,
        "vertical": vertical,
        "placement_type": placement_type,
        "location": "Remote",
        "status": "pending",
        "summary": (description or "Client draft.").split("\n")[0][:140],
        "description": description or "Client draft. Fictional.",
        "slate_sent": False,
        "slate_application_ids": [],
    }
    jobs().append(job)
    return job


def approve(job_id: str) -> dict[str, Any] | None:
    job = job_by_id(job_id)
    if job is None:
        return None
    job["status"] = "public"
    return job


def send_slate(job_id: str, application_ids: list[str]) -> dict[str, Any] | None:
    job = job_by_id(job_id)
    if job is None:
        return None
    allowed = {row["id"] for row in applications(job_id)}
    chosen = [app_id for app_id in application_ids if app_id in allowed]
    job["slate_sent"] = True
    job["slate_application_ids"] = chosen
    return job


def slate_for(job_id: str) -> list[dict[str, Any]]:
    job = job_by_id(job_id)
    if job is None or not job["slate_sent"]:
        return []
    by_id = {row["id"]: row for row in applications(job_id)}
    return [by_id[app_id] for app_id in job["slate_application_ids"] if app_id in by_id]
