from __future__ import annotations

import httpx

from deskflow.config import Settings
from deskflow.llm import try_llm_extract
from deskflow.models import CandidateProfile, EvaluateRequest, JobDescription
from deskflow.pipeline import evaluate


def test_llm_disabled_keeps_heuristic_scorer() -> None:
    request = EvaluateRequest(
        job=JobDescription(title="SDET", description="Python and pytest required."),
        candidate=CandidateProfile(name="Alex Rivera", summary="Python pytest."),
    )
    result = evaluate(request, settings=Settings(llm_api_key=""))
    assert result.scorer == "heuristic"


def test_llm_http_failure_falls_back_to_heuristic(monkeypatch) -> None:
    job = JobDescription(title="SDET", description="Python required.")
    candidate = CandidateProfile(name="Jordan Lee", summary="Manual QA.")

    class BoomClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def post(self, *args, **kwargs):
            raise httpx.ConnectError("refused")

    monkeypatch.setattr("deskflow.llm.httpx.Client", BoomClient)

    from deskflow.extract import extract_candidate, extract_job

    result = try_llm_extract(
        job,
        candidate,
        extract_job(job),
        extract_candidate(candidate),
        Settings(llm_api_key="sk-test-not-real"),
    )
    assert result is None

    response = evaluate(
        EvaluateRequest(job=job, candidate=candidate),
        settings=Settings(llm_api_key="sk-test-not-real"),
    )
    assert response.scorer == "heuristic"
    assert 0 <= response.fit_score <= 100
