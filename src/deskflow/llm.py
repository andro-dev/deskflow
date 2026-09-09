"""Optional LLM extraction. Failures always fall back to the heuristic extractor."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from deskflow.config import Settings
from deskflow.models import CandidateProfile, ExtractedCandidate, ExtractedJob, JobDescription

logger = logging.getLogger(__name__)

_SCHEMA_HINT = """
Return JSON only with keys:
job: {required_skills: [str], nice_to_have_skills: [str], min_years_experience: int|null, seniority: str|null}
candidate: {skills: [str], years_experience: number|null, seniority: str|null, highlights: [str]}
Use lowercase skill names. seniority must be one of junior, mid, senior, staff, lead, principal, or null.
Do not invent employers, people, or contact details. Sample data only.
""".strip()


def _chat_payload(job: JobDescription, candidate: CandidateProfile, model: str) -> dict[str, Any]:
    user = {
        "job_title": job.title,
        "job_description": job.description,
        "job_required_skills": job.required_skills,
        "job_nice_to_have_skills": job.nice_to_have_skills,
        "candidate_name": candidate.name,
        "candidate_headline": candidate.headline,
        "candidate_summary": candidate.summary,
        "candidate_skills": candidate.skills,
        "candidate_years": candidate.years_experience,
        "candidate_experience": [item.model_dump() for item in candidate.experience],
    }
    return {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": _SCHEMA_HINT},
            {"role": "user", "content": json.dumps(user)},
        ],
    }


def _as_str_list(value: Any, *, lowercase: bool = False) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            text = item.strip()
            out.append(text.lower() if lowercase else text)
    return out


def _as_skill_list(value: Any) -> list[str]:
    return _as_str_list(value, lowercase=True)


def _as_seniority(value: Any) -> str | None:
    allowed = {"junior", "mid", "senior", "staff", "lead", "principal"}
    if isinstance(value, str) and value.strip().lower() in allowed:
        return value.strip().lower()
    return None


def try_llm_extract(
    job: JobDescription,
    candidate: CandidateProfile,
    heuristic_job: ExtractedJob,
    heuristic_candidate: ExtractedCandidate,
    settings: Settings,
) -> tuple[ExtractedJob, ExtractedCandidate] | None:
    if not settings.llm_enabled():
        return None

    url = settings.llm_base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    try:
        with httpx.Client(timeout=settings.llm_timeout_seconds) as client:
            response = client.post(
                url,
                headers=headers,
                json=_chat_payload(job, candidate, settings.llm_model),
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            data = json.loads(content)
    except Exception as exc:  # noqa: BLE001 — any LLM failure must fall back
        logger.warning("LLM extraction failed; using heuristic fallback: %s", exc)
        return None

    job_data = data.get("job") if isinstance(data, dict) else None
    cand_data = data.get("candidate") if isinstance(data, dict) else None
    if not isinstance(job_data, dict) or not isinstance(cand_data, dict):
        logger.warning("LLM extraction returned unexpected JSON; using heuristic fallback")
        return None

    extracted_job = heuristic_job.model_copy(
        update={
            "required_skills": _as_skill_list(job_data.get("required_skills"))
            or heuristic_job.required_skills,
            "nice_to_have_skills": _as_skill_list(job_data.get("nice_to_have_skills"))
            or heuristic_job.nice_to_have_skills,
            "min_years_experience": job_data.get("min_years_experience")
            if isinstance(job_data.get("min_years_experience"), int)
            else heuristic_job.min_years_experience,
            "seniority": _as_seniority(job_data.get("seniority")) or heuristic_job.seniority,
            "source": "llm+heuristic",
        }
    )
    extracted_candidate = heuristic_candidate.model_copy(
        update={
            "skills": _as_skill_list(cand_data.get("skills")) or heuristic_candidate.skills,
            "years_experience": cand_data.get("years_experience")
            if isinstance(cand_data.get("years_experience"), (int, float))
            else heuristic_candidate.years_experience,
            "seniority": _as_seniority(cand_data.get("seniority"))
            or heuristic_candidate.seniority,
            "highlights": _as_str_list(cand_data.get("highlights"))
            or heuristic_candidate.highlights,
            "source": "llm+heuristic",
        }
    )
    return extracted_job, extracted_candidate
