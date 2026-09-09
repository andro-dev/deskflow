from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

NoteStyle = Literal["outreach", "screening"]
Recommendation = Literal["strong_fit", "possible_fit", "weak_fit"]
EvidenceKind = Literal["match", "gap", "signal"]
ScorerName = Literal["heuristic", "llm+heuristic"]
Seniority = Literal["junior", "mid", "senior", "staff", "lead", "principal"]


class ExperienceItem(BaseModel):
    title: str = ""
    organization: str = "Sample employer"
    years: float | None = None
    bullets: list[str] = Field(default_factory=list)


class JobDescription(BaseModel):
    title: str
    company: str = "Sample employer"
    description: str
    required_skills: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[str] = Field(default_factory=list)
    min_years_experience: int | None = None


class CandidateProfile(BaseModel):
    """Public sample profiles only. Do not send real resumes or personal data."""

    name: str
    headline: str = ""
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    years_experience: float | None = None
    experience: list[ExperienceItem] = Field(default_factory=list)


class EvaluateRequest(BaseModel):
    job: JobDescription
    candidate: CandidateProfile
    note_style: NoteStyle = "outreach"


class ExtractedJob(BaseModel):
    title: str
    company: str
    required_skills: list[str]
    nice_to_have_skills: list[str]
    min_years_experience: int | None
    seniority: Seniority | None
    source: ScorerName


class ExtractedCandidate(BaseModel):
    name: str
    skills: list[str]
    years_experience: float | None
    seniority: Seniority | None
    highlights: list[str]
    source: ScorerName


class EvidenceBullet(BaseModel):
    kind: EvidenceKind
    text: str


class ScoreBreakdown(BaseModel):
    required_skills: float = Field(ge=0, le=1)
    nice_to_have_skills: float = Field(ge=0, le=1)
    experience: float = Field(ge=0, le=1)
    seniority: float = Field(ge=0, le=1)
    weights: dict[str, float]


class EvaluateResponse(BaseModel):
    fit_score: int = Field(ge=0, le=100)
    recommendation: Recommendation
    evidence: list[EvidenceBullet]
    draft_note: str
    extracted_job: ExtractedJob
    extracted_candidate: ExtractedCandidate
    breakdown: ScoreBreakdown
    scorer: ScorerName


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str
    llm_configured: bool
