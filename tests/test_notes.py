from __future__ import annotations

from deskflow.models import EvidenceBullet, ExtractedCandidate, ExtractedJob
from deskflow.notes import draft_note


def test_outreach_and_screening_notes_differ() -> None:
    job = ExtractedJob(
        title="Senior Python SDET",
        company="Lumenfield Labs",
        required_skills=["python"],
        nice_to_have_skills=[],
        min_years_experience=5,
        seniority="senior",
        source="heuristic",
    )
    candidate = ExtractedCandidate(
        name="Alex Rivera",
        skills=["python"],
        years_experience=6,
        seniority="senior",
        highlights=[],
        source="heuristic",
    )
    evidence = [
        EvidenceBullet(kind="match", text="Required skill 'python' appears on both sides."),
        EvidenceBullet(kind="gap", text="Required skill 'docker' was not found."),
    ]
    outreach = draft_note(
        job=job,
        candidate=candidate,
        fit_score=81,
        recommendation="strong_fit",
        evidence=evidence,
        style="outreach",
    )
    screening = draft_note(
        job=job,
        candidate=candidate,
        fit_score=81,
        recommendation="strong_fit",
        evidence=evidence,
        style="screening",
    )
    assert outreach.startswith("Subject:")
    assert "Hi Alex" in outreach
    assert "Screening note" in screening
    assert "81/100" in outreach and "81/100" in screening
    assert "docker" in outreach and "docker" in screening
