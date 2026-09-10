from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from deskflow import __version__
from deskflow.config import get_settings
from deskflow.models import EvaluateRequest, EvaluateResponse, HealthResponse
from deskflow.pipeline import evaluate
from deskflow.proto.router import router as proto_router

SAMPLES_DIR = Path(__file__).resolve().parents[2] / "samples"

app = FastAPI(
    title="Deskflow",
    version=__version__,
    description=(
        "Staffing-desk assistant. POST a job description and a SAMPLE candidate "
        "profile; receive a fit score, evidence bullets, and a draft note. "
        "Do not submit real resumes, personal data, or employer contacts. "
        "GET / is a clickable Tekforce prototype (sample data only)."
    ),
)

app.include_router(proto_router)
app.mount(
    "/proto/static",
    StaticFiles(directory=Path(__file__).resolve().parent / "proto" / "static"),
    name="proto_static",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        version=__version__,
        llm_configured=settings.llm_enabled(),
    )


@app.post("/v1/evaluate", response_model=EvaluateResponse)
def evaluate_pair(request: EvaluateRequest) -> EvaluateResponse:
    return evaluate(request)


@app.get("/v1/samples")
def list_samples() -> JSONResponse:
    """Bundled fictional payloads for demos and tests. Not real people."""
    files = sorted(SAMPLES_DIR.glob("*.json")) if SAMPLES_DIR.is_dir() else []
    return JSONResponse(
        {
            "notice": "Sample data only. Do not replace these with real resumes.",
            "files": [path.name for path in files],
        }
    )
