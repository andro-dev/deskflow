"""Explainable fit scoring. The rubric is the product, not a hidden model."""

from __future__ import annotations

from deskflow.extract import SENIORITY_RANK, canonicalize_skill
from deskflow.models import (
    EvidenceBullet,
    ExtractedCandidate,
    ExtractedJob,
    Recommendation,
    ScoreBreakdown,
)

WEIGHTS = {
    "required_skills": 0.55,
    "nice_to_have_skills": 0.15,
    "experience": 0.20,
    "seniority": 0.10,
}


def _coverage(needed: list[str], have: list[str]) -> tuple[float, list[str], list[str]]:
    if not needed:
        return 1.0, [], []
    have_set = {canonicalize_skill(item) for item in have}
    matched = [skill for skill in needed if canonicalize_skill(skill) in have_set]
    missing = [skill for skill in needed if canonicalize_skill(skill) not in have_set]
    return len(matched) / len(needed), matched, missing


def _experience_score(required: int | None, actual: float | None) -> float:
    if required is None:
        return 1.0
    if actual is None:
        return 0.5
    if actual >= required:
        return 1.0
    return max(0.0, actual / required)


def _seniority_score(job: ExtractedJob, candidate: ExtractedCandidate) -> float:
    if job.seniority is None or candidate.seniority is None:
        return 0.8
    gap = SENIORITY_RANK[job.seniority] - SENIORITY_RANK[candidate.seniority]
    if gap <= 0:
        return 1.0
    return max(0.0, 1.0 - 0.25 * gap)


def _recommendation(score: int) -> Recommendation:
    if score >= 75:
        return "strong_fit"
    if score >= 50:
        return "possible_fit"
    return "weak_fit"


def score_fit(
    job: ExtractedJob, candidate: ExtractedCandidate
) -> tuple[int, Recommendation, list[EvidenceBullet], ScoreBreakdown]:
    required_cov, required_matched, required_missing = _coverage(
        job.required_skills, candidate.skills
    )
    nice_cov, nice_matched, _ = _coverage(job.nice_to_have_skills, candidate.skills)
    exp_score = _experience_score(job.min_years_experience, candidate.years_experience)
    sen_score = _seniority_score(job, candidate)

    raw = (
        WEIGHTS["required_skills"] * required_cov
        + WEIGHTS["nice_to_have_skills"] * nice_cov
        + WEIGHTS["experience"] * exp_score
        + WEIGHTS["seniority"] * sen_score
    )
    fit_score = int(round(100 * raw))
    fit_score = min(100, max(0, fit_score))

    evidence: list[EvidenceBullet] = []
    for skill in required_matched:
        evidence.append(
            EvidenceBullet(
                kind="match",
                text=f"Required skill '{skill}' appears on both the job and the candidate profile.",
            )
        )
    for skill in required_missing:
        evidence.append(
            EvidenceBullet(
                kind="gap",
                text=f"Required skill '{skill}' is listed on the job but was not found on the candidate profile.",
            )
        )
    for skill in nice_matched[:4]:
        evidence.append(
            EvidenceBullet(
                kind="signal",
                text=f"Nice-to-have skill '{skill}' is present on the candidate profile.",
            )
        )

    if job.min_years_experience is not None:
        years = candidate.years_experience
        if years is None:
            evidence.append(
                EvidenceBullet(
                    kind="signal",
                    text=f"Job asks for {job.min_years_experience}+ years; candidate years were not stated.",
                )
            )
        elif years >= job.min_years_experience:
            evidence.append(
                EvidenceBullet(
                    kind="match",
                    text=(
                        f"Candidate years ({years:g}) meet the job minimum "
                        f"({job.min_years_experience}+)."
                    ),
                )
            )
        else:
            evidence.append(
                EvidenceBullet(
                    kind="gap",
                    text=(
                        f"Candidate years ({years:g}) are below the job minimum "
                        f"({job.min_years_experience}+)."
                    ),
                )
            )

    if job.seniority and candidate.seniority:
        if SENIORITY_RANK[candidate.seniority] >= SENIORITY_RANK[job.seniority]:
            evidence.append(
                EvidenceBullet(
                    kind="match",
                    text=f"Seniority signal '{candidate.seniority}' meets job target '{job.seniority}'.",
                )
            )
        else:
            evidence.append(
                EvidenceBullet(
                    kind="gap",
                    text=f"Seniority signal '{candidate.seniority}' is below job target '{job.seniority}'.",
                )
            )

    if not evidence:
        evidence.append(
            EvidenceBullet(
                kind="signal",
                text="Not enough structured overlap to cite matches or gaps; score is a weak prior.",
            )
        )

    breakdown = ScoreBreakdown(
        required_skills=round(required_cov, 4),
        nice_to_have_skills=round(nice_cov, 4),
        experience=round(exp_score, 4),
        seniority=round(sen_score, 4),
        weights=dict(WEIGHTS),
    )
    return fit_score, _recommendation(fit_score), evidence, breakdown
