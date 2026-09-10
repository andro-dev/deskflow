"""Prototype data access. Jobs, catalog, and users live in SQLite (or Postgres later)."""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from deskflow.db.engine import init_db, session_factory
from deskflow.db.models import Application, Job, PlacementType, SlateItem, Vertical
from deskflow.db.seed import PLACEMENT_NAMES, VERTICAL_NAMES, sample_accounts

ROLES = ("visitor", "candidate", "client", "recruiter", "exec", "admin")

HOME_AFTER_LOGIN: dict[str, str] = {
    "candidate": "/applications",
    "client": "/me/jobs",
    "recruiter": "/desk/jobs",
    "exec": "/desk/approve",
    "admin": "/desk/users",
}

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
        ("Users", "/desk/users"),
    ),
    "admin": (
        ("Jobs", "/jobs"),
        ("Approve", "/desk/approve"),
        ("Desk", "/desk/jobs"),
        ("Users", "/desk/users"),
    ),
}


def VERTICALS() -> tuple[str, ...]:
    db = session_factory()()
    try:
        rows = db.scalars(select(Vertical).order_by(Vertical.sort_order)).all()
        return tuple(row.name for row in rows) or VERTICAL_NAMES
    finally:
        db.close()


def PLACEMENT_TYPES() -> tuple[str, ...]:
    db = session_factory()()
    try:
        rows = db.scalars(select(PlacementType).order_by(PlacementType.sort_order)).all()
        return tuple(row.name for row in rows) or PLACEMENT_NAMES
    finally:
        db.close()


def account_for_email(email: str) -> dict[str, str] | None:
    needle = email.strip().lower()
    return next((row for row in sample_accounts() if row["email"] == needle), None)


def my_tekforce_href(persona: str) -> str:
    if persona == "visitor":
        return "/my-tekforce/login"
    return "/my-tekforce"


def reset() -> None:
    init_db(drop=True)


def _job_dict(job: Job) -> dict[str, Any]:
    items = sorted(job.slate_items, key=lambda row: row.sort_order)
    return {
        "id": job.id,
        "title": job.title,
        "account": job.account,
        "vertical": job.vertical.name,
        "placement_type": job.placement_type.name,
        "location": job.location,
        "status": job.status,
        "summary": job.summary,
        "description": job.description,
        "slate_sent": job.slate_sent,
        "slate_application_ids": [item.application_id for item in items],
    }


def _app_dict(row: Application, job: Job | None = None) -> dict[str, Any]:
    payload = {
        "id": row.id,
        "job_id": row.job_id,
        "candidate_name": row.candidate_name,
        "headline": row.headline,
        "stage": row.stage,
        "fit_score": row.fit_score,
        "recommendation": row.recommendation,
        "owner": row.owner,
    }
    if job is not None:
        payload["job"] = _job_dict(job)
    return payload


def _job_query():
    return select(Job).options(
        selectinload(Job.vertical),
        selectinload(Job.placement_type),
        selectinload(Job.slate_items),
    )


def jobs() -> list[dict[str, Any]]:
    db = session_factory()()
    try:
        rows = db.scalars(_job_query().order_by(Job.title)).all()
        return [_job_dict(job) for job in rows]
    finally:
        db.close()


def job_by_id(job_id: str) -> dict[str, Any] | None:
    db = session_factory()()
    try:
        job = db.scalar(_job_query().where(Job.id == job_id))
        return _job_dict(job) if job else None
    finally:
        db.close()


def public_jobs(query: str = "") -> list[dict[str, Any]]:
    rows = [job for job in jobs() if job["status"] == "public"]
    needle = query.strip().lower()
    if not needle:
        return rows
    return [
        job
        for job in rows
        if needle in job["title"].lower()
        or needle in job["summary"].lower()
        or needle in job["vertical"].lower()
        or needle in job["account"].lower()
    ]


def pending_jobs() -> list[dict[str, Any]]:
    return [job for job in jobs() if job["status"] == "pending"]


def applications(job_id: str | None = None) -> list[dict[str, Any]]:
    db = session_factory()()
    try:
        stmt = select(Application)
        if job_id is not None:
            stmt = stmt.where(Application.job_id == job_id)
        rows = db.scalars(stmt).all()
        return [_app_dict(row) for row in rows]
    finally:
        db.close()


def candidate_applications() -> list[dict[str, Any]]:
    db = session_factory()()
    try:
        rows = db.scalars(select(Application)).all()
        result = []
        for row in rows:
            if row.candidate_name == "Alex Rivera" or row.owner == "candidate":
                job = db.scalar(_job_query().where(Job.id == row.job_id))
                result.append(_app_dict(row, job))
        return result
    finally:
        db.close()


def already_applied(job_id: str, name: str) -> bool:
    return any(
        row["job_id"] == job_id and row["candidate_name"] == name for row in applications()
    )


def apply(job_id: str, name: str, headline: str) -> dict[str, Any] | None:
    db = session_factory()()
    try:
        job = db.scalar(_job_query().where(Job.id == job_id))
        if job is None or job.status != "public":
            return None
        existing = db.scalar(
            select(Application).where(
                Application.job_id == job_id, Application.candidate_name == name
            )
        )
        if existing is not None:
            return _app_dict(existing)
        row = Application(
            id=f"app-{uuid.uuid4().hex[:12]}",
            job_id=job_id,
            candidate_name=name,
            headline=headline or "Candidate",
            stage="Applied",
            fit_score=None,
            recommendation=None,
            owner="candidate",
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return _app_dict(row)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def draft_job(
    title: str,
    vertical: str,
    placement_type: str,
    description: str,
    account: str = "Lumenfield Labs",
) -> dict[str, Any]:
    db = session_factory()()
    try:
        vert = db.scalar(select(Vertical).where(Vertical.name == vertical))
        place = db.scalar(select(PlacementType).where(PlacementType.name == placement_type))
        if vert is None or place is None:
            raise ValueError("Unknown vertical or placement type")
        job = Job(
            id=f"job-{uuid.uuid4().hex[:12]}",
            title=title,
            account=account,
            vertical_id=vert.id,
            placement_type_id=place.id,
            location="Remote",
            status="pending",
            summary=(description or "Client draft.").split("\n")[0][:140],
            description=description or "Client draft. Fictional.",
            slate_sent=False,
        )
        db.add(job)
        db.commit()
        loaded = db.scalar(_job_query().where(Job.id == job.id))
        assert loaded is not None
        return _job_dict(loaded)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def approve(job_id: str) -> dict[str, Any] | None:
    db = session_factory()()
    try:
        job = db.scalar(_job_query().where(Job.id == job_id))
        if job is None:
            return None
        job.status = "public"
        db.commit()
        db.refresh(job)
        return _job_dict(job)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def send_slate(job_id: str, application_ids: list[str]) -> dict[str, Any] | None:
    db = session_factory()()
    try:
        job = db.scalar(_job_query().where(Job.id == job_id))
        if job is None:
            return None
        allowed = {
            row.id
            for row in db.scalars(
                select(Application).where(Application.job_id == job_id)
            ).all()
        }
        chosen = [app_id for app_id in application_ids if app_id in allowed]
        db.execute(delete(SlateItem).where(SlateItem.job_id == job_id))
        for index, app_id in enumerate(chosen):
            db.add(SlateItem(job_id=job_id, application_id=app_id, sort_order=index))
        job.slate_sent = True
        db.commit()
        loaded = db.scalar(_job_query().where(Job.id == job_id))
        assert loaded is not None
        return _job_dict(loaded)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def slate_for(job_id: str) -> list[dict[str, Any]]:
    job = job_by_id(job_id)
    if job is None or not job["slate_sent"]:
        return []
    by_id = {row["id"]: row for row in applications(job_id)}
    return [by_id[app_id] for app_id in job["slate_application_ids"] if app_id in by_id]
