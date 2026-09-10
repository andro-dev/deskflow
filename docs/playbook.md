# How Deskflow is built with Cursor

This is the engineering playbook for **this product**, not a general AI tutorial. The public repo should look like a service someone reviewed, not a chat log.

## Goal of the workflow

Agents accelerate boilerplate, tests, and first-pass docs. A human owns:

- the scoring rubric
- the sample-data policy
- what gets merged
- what gets deployed

If you cannot explain a change without the agent, it is not ready.

## Working loop

1. **Scope the change in a sentence.** Example: “Extract nice-to-have skills from a JD heading, then add an API test.” If the sentence needs “and also,” split the PR.
2. **Point the agent at files, not vibes.** Name `src/deskflow/score.py`, `tests/test_api.py`, and the sample JSON it should use.
3. **Generate the patch.** Prefer the agent editing this repo over pasting code from a chat window.
4. **Review like a junior’s PR.** Read the diff. Run `pytest`. Hit the endpoint with `samples/strong_fit_sdet.json` and `samples/weak_fit_manual_qa.json`. Check that the weak sample still scores lower.
5. **Keep the PR small.** CI (`.github/workflows/ci.yml`) is the merge gate: unit/API tests and a Docker build. Do not bundle a rubric rewrite with a Dockerfile tweak unless they are the same bug.

## What “agent-style” means here

Deskflow’s agent feature is **structured extraction**, not a chatbot.

- Heuristic path: catalog match + years/seniority parse. Always available.
- Optional LLM path: may replace extracted fields when a key is present.
- Scoring: always `score.py`. The model does not get to invent the fit number.

That split is intentional. It is testable, it works offline, and it is the answer to “how do you use agents without shipping garbage?”

## What we refuse to let the agent do

| Refusal | Why |
| --- | --- |
| Real resumes, PII, hiring-manager names | This repo is public. Fiction lives in `samples/`. |
| Pushing to origin or skipping hooks | Humans decide when history leaves the machine. |
| A fake AWS URL | If credentials are missing, document App Runner steps; do not invent a hostname. |
| Unbounded LLM scoring | A demo that needs a paid key is not an MVP. |
| Implementing the wiki (ATS/CRM) or Kubernetes / a second language | Product vision is `docs/wiki/`. Do not build it unless a human asks. The running MVP is still one API and tests. |
| Deleting or weakening tests to go green | The SDET artifact is `tests/test_api.py`. Protect it. |
| Committing `.env` or cloud keys | Local Docker and pytest must work without secrets. |

If the agent proposes any of the above, the review answer is no.

## Review checklist (copy into a PR)

- [ ] Sample payloads only; no real candidate data
- [ ] `pytest` green locally
- [ ] Heuristic path works with LLM env vars unset
- [ ] Fit score still 0–100 with evidence + draft note
- [ ] Docs match the operator path you actually used (local, Docker, AWS steps)
- [ ] No new cloud, language, or database unless requested

## Interview demo

Show three things, in order:

1. `pytest` (especially `tests/test_api.py`)
2. `POST /v1/evaluate` on both sample files
3. `score.py` weights and the LLM fallback in `llm.py`

That is the product. The playbook exists so the workflow is as demoable as the code.
