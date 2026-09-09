"""Deterministic extraction of skills, years, and seniority from free text."""

from __future__ import annotations

import re
from typing import Iterable

from deskflow.catalog import SKILLS
from deskflow.models import (
    CandidateProfile,
    ExtractedCandidate,
    ExtractedJob,
    JobDescription,
    Seniority,
)

SENIORITY_RANK: dict[Seniority, int] = {
    "junior": 1,
    "mid": 2,
    "senior": 3,
    "staff": 4,
    "lead": 4,
    "principal": 5,
}

_SENIORITY_PATTERNS: tuple[tuple[re.Pattern[str], Seniority], ...] = (
    (re.compile(r"\bprincipal\b", re.I), "principal"),
    (re.compile(r"\bstaff\b", re.I), "staff"),
    (re.compile(r"\blead\b", re.I), "lead"),
    (re.compile(r"\bsenior\b|\bsr\.?\b", re.I), "senior"),
    (re.compile(r"\bmid[- ]?level\b|\bintermediate\b|\bmid[- ]senior\b", re.I), "mid"),
    (re.compile(r"\bjunior\b|\bjr\.?\b|\bentry[- ]level\b", re.I), "junior"),
)

_YEARS_RE = re.compile(
    r"(?:at least\s+|minimum(?: of)?\s+)?(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs)\b",
    re.I,
)

_NICE_HEADING = re.compile(
    r"^(nice[- ]to[- ]have|preferred(?: qualifications)?|bonus|plus(?:es)?)\b.*$",
    re.I | re.M,
)
_REQUIRED_HEADING = re.compile(
    r"^(required|must[- ]haves?|minimum qualifications|what you.?ll need|responsibilities)\b.*$",
    re.I | re.M,
)


def normalize_skill(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def canonicalize_skill(value: str) -> str:
    """Map aliases (pytest, FastAPI, AWS) onto catalog names when possible."""
    norm = normalize_skill(value)
    if not norm:
        return ""
    haystack = f" {norm} "
    for skill in SKILLS:
        if norm == skill.canonical or any(
            _phrase_in_text(alias.lower(), haystack) for alias in skill.aliases
        ):
            return skill.canonical
    return norm


def _phrase_in_text(phrase: str, haystack: str) -> bool:
    if phrase == " go ":
        return bool(re.search(r"(^|[^a-z])go([^a-z]|$)", haystack))
    escaped = re.escape(phrase)
    return re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", haystack) is not None


def detect_skills(text: str) -> list[str]:
    haystack = f" {text.lower()} "
    found: list[str] = []
    seen: set[str] = set()
    for skill in SKILLS:
        if any(_phrase_in_text(alias.lower(), haystack) for alias in skill.aliases):
            if skill.canonical not in seen:
                seen.add(skill.canonical)
                found.append(skill.canonical)
    return found


def detect_years(text: str) -> int | None:
    matches = [float(match.group(1)) for match in _YEARS_RE.finditer(text)]
    if not matches:
        return None
    return int(max(matches))


def detect_seniority(*parts: str) -> Seniority | None:
    blob = " ".join(part for part in parts if part)
    for pattern, label in _SENIORITY_PATTERNS:
        if pattern.search(blob):
            return label
    return None


def _split_job_sections(description: str) -> tuple[str, str]:
    nice_match = _NICE_HEADING.search(description)
    if not nice_match:
        return description, ""
    required_text = description[: nice_match.start()]
    nice_text = description[nice_match.start() :]
    required_heading = _REQUIRED_HEADING.search(required_text)
    if required_heading:
        required_text = required_text[required_heading.start() :]
    return required_text, nice_text


def _merge_unique(primary: Iterable[str], extra: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for raw in [*primary, *extra]:
        item = canonicalize_skill(raw)
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def extract_job(job: JobDescription) -> ExtractedJob:
    required_section, nice_section = _split_job_sections(job.description)
    inferred_required = detect_skills(required_section or job.description)
    inferred_nice = detect_skills(nice_section) if nice_section else []
    inferred_nice = [skill for skill in inferred_nice if skill not in inferred_required]

    required = (
        [normalize_skill(item) for item in job.required_skills if item.strip()]
        if job.required_skills
        else inferred_required
    )
    nice = (
        [normalize_skill(item) for item in job.nice_to_have_skills if item.strip()]
        if job.nice_to_have_skills
        else inferred_nice
    )
    nice = [skill for skill in nice if skill not in required]

    years = job.min_years_experience
    if years is None:
        years = detect_years(job.description)

    return ExtractedJob(
        title=job.title.strip(),
        company=job.company.strip() or "Sample employer",
        required_skills=_merge_unique(required, []),
        nice_to_have_skills=_merge_unique(nice, []),
        min_years_experience=years,
        seniority=detect_seniority(job.title, job.description),
        source="heuristic",
    )


def extract_candidate(candidate: CandidateProfile) -> ExtractedCandidate:
    experience_text = " ".join(
        " ".join([item.title, item.organization, *item.bullets])
        for item in candidate.experience
    )
    blob = " ".join(
        part
        for part in [candidate.headline, candidate.summary, experience_text, *candidate.skills]
        if part
    )
    inferred = detect_skills(blob)
    declared = [normalize_skill(item) for item in candidate.skills if item.strip()]
    skills = _merge_unique(declared, inferred)

    years = candidate.years_experience
    if years is None:
        summed = sum(item.years or 0 for item in candidate.experience)
        years = summed if summed else detect_years(blob)

    highlights: list[str] = []
    if candidate.headline:
        highlights.append(candidate.headline.strip())
    for item in candidate.experience:
        if item.title:
            org = item.organization or "Sample employer"
            highlights.append(f"{item.title} at {org}")
        highlights.extend(item.bullets[:2])

    return ExtractedCandidate(
        name=candidate.name.strip(),
        skills=skills,
        years_experience=float(years) if years is not None else None,
        seniority=detect_seniority(candidate.headline, candidate.summary, experience_text),
        highlights=highlights[:6],
        source="heuristic",
    )
