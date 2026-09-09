"""Evaluate pipeline: extract → optional LLM overlay → score → draft note."""

from __future__ import annotations

from deskflow.config import Settings, get_settings
from deskflow.extract import extract_candidate, extract_job
from deskflow.llm import try_llm_extract
from deskflow.models import EvaluateRequest, EvaluateResponse
from deskflow.notes import draft_note
from deskflow.score import score_fit


def evaluate(request: EvaluateRequest, settings: Settings | None = None) -> EvaluateResponse:
    settings = settings or get_settings()
    job = extract_job(request.job)
    candidate = extract_candidate(request.candidate)

    llm_result = try_llm_extract(request.job, request.candidate, job, candidate, settings)
    if llm_result is not None:
        job, candidate = llm_result
        scorer_name = "llm+heuristic"
    else:
        scorer_name = "heuristic"

    fit_score, recommendation, evidence, breakdown = score_fit(job, candidate)
    note = draft_note(
        job=job,
        candidate=candidate,
        fit_score=fit_score,
        recommendation=recommendation,
        evidence=evidence,
        style=request.note_style,
    )
    return EvaluateResponse(
        fit_score=fit_score,
        recommendation=recommendation,
        evidence=evidence,
        draft_note=note,
        extracted_job=job,
        extracted_candidate=candidate,
        breakdown=breakdown,
        scorer=scorer_name,
    )
