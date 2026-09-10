from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from deskflow.db.engine import session_factory
from deskflow.db.models import (
    Application,
    Job,
    PlacementType,
    PipelineStage,
    Role,
    User,
    UserRole,
    Vertical,
)
from deskflow.db.passwords import DEMO_PASSWORD, hash_password

ROLE_ROWS = (
    ("candidate", "Candidate"),
    ("client", "Client"),
    ("recruiter", "Recruiter"),
    ("exec", "Exec"),
    ("admin", "Admin"),
)

VERTICAL_NAMES = (
    "IT",
    "CEO Search",
    "Medical",
    "Financial",
    "Legal",
    "Skilled trades",
)

PLACEMENT_NAMES = (
    "Contract",
    "Contract-to-hire",
    "Permanent",
    "Executive search",
)

STAGE_NAMES = (
    "Applied",
    "Screening",
    "Interview",
    "Offer",
    "Hired",
    "Rejected",
)

SAMPLE_USERS = (
    ("alex.rivera@example.com", "Alex Rivera", "candidate", "Candidate"),
    ("morgan.hale@lumenfield.example", "Morgan Hale", "client", "Client · Lumenfield Labs"),
    ("sam.okonkwo@tekforce.example", "Sam Okonkwo", "recruiter", "Recruiter"),
    ("exec@tekforce.example", "Exec", "exec", "Exec"),
)


def seed_if_empty() -> None:
    db = session_factory()()
    try:
        if db.scalar(select(Role.id).limit(1)) is not None:
            return
        _seed(db)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _seed(db: Session) -> None:
    roles = {code: Role(code=code, label=label) for code, label in ROLE_ROWS}
    db.add_all(roles.values())
    db.flush()

    verticals = {
        name: Vertical(name=name, sort_order=i) for i, name in enumerate(VERTICAL_NAMES)
    }
    db.add_all(verticals.values())
    placements = {
        name: PlacementType(name=name, sort_order=i)
        for i, name in enumerate(PLACEMENT_NAMES)
    }
    db.add_all(placements.values())
    db.add_all(
        [
            PipelineStage(name=name, sort_order=i)
            for i, name in enumerate(STAGE_NAMES)
        ]
    )
    db.flush()

    password_hash = hash_password(DEMO_PASSWORD)
    users: dict[str, User] = {}
    for email, name, role_code, _label in SAMPLE_USERS:
        user = User(email=email, name=name, password_hash=password_hash, active=True)
        db.add(user)
        db.flush()
        db.add(UserRole(user_id=user.id, role_id=roles[role_code].id))
        users[email] = user

    sdet = Job(
        id="sdet",
        title="Senior Python SDET",
        account="Lumenfield Labs",
        vertical_id=verticals["IT"].id,
        placement_type_id=placements["Permanent"].id,
        location="Remote",
        status="public",
        summary="Build and own API tests for internal Python services. Sample role only.",
        description=(
            "Lumenfield Labs (fictional) is hiring a Senior Python SDET for internal "
            "developer tools.\n\nRequired: Python, pytest, API testing, FastAPI, "
            "GitHub Actions, Docker.\nNice to have: Playwright, AWS, SQL."
        ),
        slate_sent=False,
    )
    controller = Job(
        id="controller",
        title="Controller",
        account="Lumenfield Labs",
        vertical_id=verticals["Financial"].id,
        placement_type_id=placements["Permanent"].id,
        location="New York, NY",
        status="pending",
        summary="Own close, controls, and reporting for a small operating company.",
        description=(
            "Client draft. Needs Tekforce approval before it appears on the public board. "
            "Fictional req for the prototype loop."
        ),
        slate_sent=False,
    )
    db.add_all([sdet, controller])
    db.flush()

    db.add_all(
        [
            Application(
                id="app-alex-sdet",
                job_id="sdet",
                user_id=users["alex.rivera@example.com"].id,
                candidate_name="Alex Rivera",
                headline="Senior test engineer, Python automation",
                stage="Screening",
                fit_score=86,
                recommendation="strong_fit",
                owner="candidate",
            ),
            Application(
                id="app-jordan-sdet",
                job_id="sdet",
                user_id=None,
                candidate_name="Jordan Lee",
                headline="Manual QA, documentation",
                stage="Applied",
                fit_score=31,
                recommendation="weak_fit",
                owner="recruiter",
            ),
        ]
    )


def sample_accounts() -> list[dict[str, str]]:
    return [
        {"email": email, "name": name, "role": role, "label": label}
        for email, name, role, label in SAMPLE_USERS
    ]
