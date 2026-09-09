from __future__ import annotations

from deskflow.extract import (
    detect_skills,
    detect_years,
    extract_candidate,
    extract_job,
)
from deskflow.models import CandidateProfile, JobDescription


def test_detect_skills_finds_catalog_aliases() -> None:
    text = "We use FastAPI, py.test, GitHub Actions, and Amazon Web Services."
    skills = detect_skills(text)
    assert "fastapi" in skills
    assert "pytest" in skills
    assert "github actions" in skills
    assert "aws" in skills


def test_detect_years_reads_minimum() -> None:
    assert detect_years("Looking for at least 5 years of Python testing.") == 5
    assert detect_years("No numeric experience stated.") is None


def test_extract_job_splits_required_and_nice_to_have() -> None:
    job = JobDescription(
        title="Senior Python SDET",
        company="Lumenfield Labs",
        description=(
            "Required:\nPython, pytest, Docker\n\n"
            "Nice to have:\nPlaywright and SQL\n"
        ),
    )
    extracted = extract_job(job)
    assert extracted.seniority == "senior"
    assert "python" in extracted.required_skills
    assert "pytest" in extracted.required_skills
    assert "docker" in extracted.required_skills
    assert "playwright" in extracted.nice_to_have_skills
    assert "sql" in extracted.nice_to_have_skills
    assert "playwright" not in extracted.required_skills
    assert extracted.source == "heuristic"


def test_extract_job_honors_explicit_skill_lists() -> None:
    job = JobDescription(
        title="SDET",
        description="A vague paragraph that never names the stack.",
        required_skills=["Python", "pytest"],
        nice_to_have_skills=["Playwright"],
        min_years_experience=4,
    )
    extracted = extract_job(job)
    assert extracted.required_skills == ["python", "pytest"]
    assert extracted.nice_to_have_skills == ["playwright"]
    assert extracted.min_years_experience == 4


def test_extract_candidate_merges_declared_and_inferred_skills() -> None:
    candidate = CandidateProfile(
        name="Alex Rivera",
        headline="Senior SDET",
        summary="Built FastAPI contract tests.",
        skills=["Python"],
        experience=[],
    )
    extracted = extract_candidate(candidate)
    assert extracted.name == "Alex Rivera"
    assert "python" in extracted.skills
    assert "fastapi" in extracted.skills
    assert extracted.seniority == "senior"
