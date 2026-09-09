from __future__ import annotations

from deskflow.models import ExtractedCandidate, ExtractedJob
from deskflow.score import WEIGHTS, score_fit


def _job(**overrides) -> ExtractedJob:
    payload = {
        "title": "Senior Python SDET",
        "company": "Lumenfield Labs",
        "required_skills": ["python", "pytest", "docker"],
        "nice_to_have_skills": ["playwright"],
        "min_years_experience": 5,
        "seniority": "senior",
        "source": "heuristic",
    }
    payload.update(overrides)
    return ExtractedJob(**payload)


def _candidate(**overrides) -> ExtractedCandidate:
    payload = {
        "name": "Alex Rivera",
        "skills": ["python", "pytest", "docker", "playwright"],
        "years_experience": 6,
        "seniority": "senior",
        "highlights": ["Sample highlight"],
        "source": "heuristic",
    }
    payload.update(overrides)
    return ExtractedCandidate(**payload)


def test_weights_sum_to_one() -> None:
    assert round(sum(WEIGHTS.values()), 2) == 1.0


def test_full_match_is_strong_fit() -> None:
    score, recommendation, evidence, breakdown = score_fit(_job(), _candidate())
    assert score >= 75
    assert recommendation == "strong_fit"
    assert breakdown.required_skills == 1.0
    assert any(item.kind == "match" for item in evidence)
    assert not any(
        item.kind == "gap" and "python" in item.text for item in evidence
    )


def test_missing_required_skills_create_gaps_and_lower_score() -> None:
    strong, _, _, _ = score_fit(_job(), _candidate())
    weak, recommendation, evidence, breakdown = score_fit(
        _job(),
        _candidate(skills=["jira"], years_experience=2, seniority="junior"),
    )
    assert weak < strong
    assert recommendation == "weak_fit"
    assert breakdown.required_skills == 0.0
    assert any(item.kind == "gap" for item in evidence)


def test_experience_below_minimum_is_a_gap() -> None:
    _, _, evidence, breakdown = score_fit(
        _job(min_years_experience=8),
        _candidate(years_experience=3),
    )
    assert breakdown.experience < 1.0
    assert any("below the job minimum" in item.text for item in evidence)
