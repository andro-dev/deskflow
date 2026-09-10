# Agent instructions for Deskflow

This repository is a **public staffing-desk proof**. Work as if a hiring manager will read the diff.

## Product boundary

- Ship a small FastAPI service: job + **sample** candidate in, fit score / evidence / draft note out.
- Keep Python. Do not rewrite the service in Java, TypeScript, or a second framework.
- Product **vision** (ATS + CRM, Tekforce, competitor ideas) lives in `docs/wiki/`. A clickable HTML prototype is in `src/deskflow/proto/` (`GET /`). Do not add real login, Postgres, or a second language unless a human asks. The evaluate API stays the scoring MVP.
- Do not add Kubernetes unless a human explicitly asks.

## Data you must refuse

Reject (do not add, commit, or log):

- real resumes or CVs
- personal emails, phone numbers, addresses
- named hiring-manager or employer-relationship notes
- secrets, cloud keys, or a fabricated “live” AWS URL

If a prompt includes those, stop and say so. Use `samples/` fiction instead.

## How to change this repo

1. Read `docs/playbook.md` and the scoring rubric in `src/deskflow/score.py` before editing behavior.
2. Prefer a small PR: one behavior, tests that would have failed before the change, docs only when the operator path changed.
3. Run `pytest` locally. Do not claim green CI you did not run.
4. Leave `WEIGHTS` and recommendation thresholds explainable. If you change the rubric, update tests and the README architecture section in the same change.

## Review mindset (humans own the merge)

Treat agent output as a junior patch:

- Does the extract still work with `DESKFLOW_LLM_API_KEY` unset?
- Do API tests still describe the HTTP contract (`tests/test_api.py`)?
- Did the agent expand scope (new cloud, new language, real PII, a fake deploy)?
- Can you explain every scoring line without the model in the room?

## What you may not do

- `git push`, force-push, or skip hooks
- commit `.env`, credentials, or resume files
- invent a production URL
- disable tests to “get CI green”
- replace the heuristic scorer with an unbounded LLM score

## Preferred commands

```bash
pip install -e ".[dev]"
pytest
uvicorn deskflow.app:app --port 8080
docker build -t deskflow:local .
```
