"""Draft recruiter outreach and internal screening notes from scored evidence."""

from __future__ import annotations

from deskflow.models import (
    EvidenceBullet,
    ExtractedCandidate,
    ExtractedJob,
    NoteStyle,
    Recommendation,
)


def _matches(evidence: list[EvidenceBullet]) -> list[str]:
    return [item.text for item in evidence if item.kind == "match"]


def _gaps(evidence: list[EvidenceBullet]) -> list[str]:
    return [item.text for item in evidence if item.kind == "gap"]


def _bullets(lines: list[str], empty: str) -> str:
    if not lines:
        return f"- {empty}"
    return "\n".join(f"- {line}" for line in lines[:5])


def draft_note(
    *,
    job: ExtractedJob,
    candidate: ExtractedCandidate,
    fit_score: int,
    recommendation: Recommendation,
    evidence: list[EvidenceBullet],
    style: NoteStyle,
) -> str:
    rec_label = recommendation.replace("_", " ")
    if style == "outreach":
        return (
            f"Subject: {job.title} at {job.company} — possible fit\n\n"
            f"Hi {candidate.name.split()[0]},\n\n"
            f"I'm reviewing a {job.title} opening at {job.company} and your profile "
            f"looks like a {rec_label} (desk score {fit_score}/100). "
            "This note is a draft from sample data, not a live outreach.\n\n"
            "Why I'm reaching out:\n"
            f"{_bullets(_matches(evidence), 'I would like to learn more about your recent work.')}\n\n"
            "I'd like to sanity-check a couple of gaps before looping in the hiring team:\n"
            f"{_bullets(_gaps(evidence), 'No hard gaps jumped out of the structured extract.')}\n\n"
            "If you are open to a 20-minute screen, reply with two times this week.\n\n"
            "Thanks,\nDeskflow recruiter (sample)\n"
        )

    return (
        f"Screening note — {candidate.name} for {job.title} ({job.company})\n\n"
        f"Fit score: {fit_score}/100 ({rec_label}). Scorer used structured extract + published rubric.\n\n"
        "Advance signals:\n"
        f"{_bullets(_matches(evidence), 'No strong structured matches; treat as a conversation, not a yes.')}\n\n"
        "Gaps to probe:\n"
        f"{_bullets(_gaps(evidence), 'No structured gaps; confirm years, stack depth, and test ownership.')}\n\n"
        "Suggested screen questions:\n"
        "- Walk through a production test or API you owned end to end.\n"
        "- How do you decide what not to automate?\n"
        "- What would you verify before trusting an agent-generated score like this one?\n"
    )
