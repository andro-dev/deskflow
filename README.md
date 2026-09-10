# Deskflow

Staffing-desk assistant: score a **sample** candidate against a job description and draft outreach or screening notes.

This is a small public proof service. It is not a production ATS, not a resume database, and not a place for real people or real employer contacts.

**Where this is going:** Tekforce LLC will grow this into a staffing eBusiness (public two-door site, ATS + CRM, configurable verticals). The product wiki is [`docs/wiki/`](docs/wiki/README.md) — brief, competitor ideas, target architecture, and [tools evaluation](docs/wiki/tools/README.md). The running code is still this evaluate API until a slice is explicitly built.

## What it does

`POST /v1/evaluate` accepts:

- a job description (title + free text; optional explicit skill lists)
- a **fictional** candidate profile
- a note style: `outreach` or `screening`

It returns:

- a fit score from 0–100 and a recommendation (`strong_fit`, `possible_fit`, `weak_fit`)
- evidence bullets (`match`, `gap`, `signal`)
- a draft note
- the structured extract the scorer actually used

The agent-style piece is **structured extraction**, then a published rubric. An LLM may overlay the extract when `DESKFLOW_LLM_API_KEY` is set. Scoring stays on the rubric. If the key is missing or the model call fails, the deterministic heuristic runs unchanged. **No paid API key is required.**

## Architecture

```
                    ┌──────────────────────────┐
  Job + candidate   │         FastAPI          │
  POST /v1/evaluate │  /health  /v1/samples    │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │        pipeline          │
                    │  extract → score → note  │
                    └─┬──────────┬───────────┬─┘
                      │          │           │
              ┌───────▼──┐  ┌────▼────┐  ┌───▼────┐
              │ heuristic│  │ optional│  │  draft │
              │ catalog  │  │   LLM   │  │  note  │
              │ extract  │  │ overlay │  │        │
              └───────┬──┘  └────┬────┘  └────────┘
                      │          │
                      └────┬─────┘
                           │ on success: replace
                           │ extracted fields only
                    ┌──────▼──────┐
                    │   rubric    │
                    │ 55% required│
                    │ 15% nice    │
                    │ 20% years   │
                    │ 10% seniority│
                    └─────────────┘
```

Layout:

| Path | Role |
| --- | --- |
| `src/deskflow/app.py` | HTTP surface |
| `src/deskflow/extract.py` | Skill catalog + years/seniority parsing |
| `src/deskflow/llm.py` | Optional extraction overlay |
| `src/deskflow/score.py` | Fit rubric and evidence |
| `src/deskflow/notes.py` | Outreach / screening drafts |
| `tests/test_api.py` | SDET artifact: HTTP contract tests |
| `samples/` | Fictional payloads only |
| `docs/aws-deploy.md` | App Runner from ECR |
| `docs/playbook.md` | How this repo is built with agents |
| `docs/wiki/` | **Product wiki:** Tekforce brief, competitor ideas, architecture, tools evaluation |
| `AGENTS.md` | What an agent may and may not do here |

## Sample data policy

Use the files in `samples/`. Names such as **Alex Rivera** and **Jordan Lee**, and the employer **Lumenfield Labs**, are fictional.

Do not commit real resumes, personal emails, phone numbers, or named hiring-manager contacts.

## Run locally

Python 3.11+ (3.12 is what CI and Docker use).

```bash
cd /home/andrew/projects/deskflow
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn deskflow.app:app --reload --port 8080
```

Health check: `GET http://127.0.0.1:8080/health`

Evaluate the strong sample:

```bash
curl -sS http://127.0.0.1:8080/v1/evaluate \
  -H 'content-type: application/json' \
  --data @samples/strong_fit_sdet.json
```

## Run tests

```bash
cd /home/andrew/projects/deskflow
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

CI runs the same `pytest` invocation on GitHub Actions (`.github/workflows/ci.yml`) plus a Docker image build.

## Run Docker

```bash
cd /home/andrew/projects/deskflow
docker build -t deskflow:local .
docker run --rm -p 8080:8080 deskflow:local
```

Then `curl http://127.0.0.1:8080/health`. The container listens on `PORT` (default `8080`) so AWS App Runner can override it.

## AWS

There is **no live AWS URL in this repo**. Credentials were not used to deploy. Follow [docs/aws-deploy.md](docs/aws-deploy.md) for App Runner + ECR — the smallest AWS option that is still easy to explain in an interview.

## Optional LLM

Copy `.env.example`. Set `DESKFLOW_LLM_API_KEY` only if you want the model to propose extracted fields. Leave it unset for the default heuristic path.

## License

Source in this repository is available for portfolio and interview use. Treat sample profiles as fiction.
