---
updated: 2026-09-10
---

# Frontend prototype

Clickable screens so **Andrew** can feel the product. HTML/CSS on FastAPI (`GET /`). Sample data is fictional. The evaluate API is unchanged.

Users, roles, catalog, jobs, applications, and slates persist in **SQLite** (`data/deskflow.sqlite`) via portable SQLAlchemy. Restart keeps the loop. Same models can run on Postgres later (`DESKFLOW_DATABASE_URL`).

## Locked (interview 2026-09-09, DB 2026-09-10)

| Decision | Choice |
| --- | --- |
| Audience | Andrew (walk the loop himself) |
| Fidelity | Clickable screens, sample data |
| Scope | **Full loop** in one prototype |
| Look | **Motion Recruitment** layout, Work Sans, dropdowns (see [design-references.md](ideas/design-references.md)) |
| Stack | HTML/CSS served by FastAPI + SQLAlchemy |
| Auth | **View as** plus **My Tekforce** (account icon; name under it when signed in). Demo password `sample`. Sample-account buttons in Dev/Test only. |
| Role assignment | Exec/Admin page `/desk/users` |
| Brand on the site | Tekforce |
| Mobile | **later** — desktop first |
| Database | SQLite now, Postgres-ready (no JSONB/ARRAY/ENUM) |

## Full loop (must click)

Public two doors → candidate applies → client drafts a job → exec/recruiter **approves** → recruiter sends a **slate**. Switch persona between steps or log in.

Pages:

1. Home (two doors: Find work / Hire talent)
2. Job board + job detail + apply (candidate)
3. My applications (candidate)
4. Draft job / hire request (client)
5. Approve queue (exec / recruiter)
6. Job + pipeline + send slate (recruiter)
7. My jobs / slate (client)
8. My Tekforce · Log in / Register / Forgot
9. Desk · Users (assign roles)

Verticals and placement types are catalog **rows**. Sample names only (same policy as `samples/`).

## Look

* **Public:** Motion Recruitment structure — slate header, Work Sans, green CTAs, Find a Job / Hire talent dropdowns, dark hero, search card. Tekforce wordmark only; no Motion photography or logo.
* **My Tekforce:** same chrome; account icon; signed-in name under My Tekforce; green Sign in; inactive Google/Facebook/LinkedIn. Sample logins when `DESKFLOW_ENV` is `dev` or `test`.
* **Desk (approve / slate):** same header (Desk dropdown for staff), quieter tables. Not a marketing hero.

## Out of this prototype

* OAuth (Facebook/Google/LinkedIn — buttons show, inactive), email verify, production password policy
* Permission **grant** rows (roles are named bundles for nav)
* Accounts/contacts CRM, placements, evaluations table, outbox
* Docker Postgres / RDS (engine supports it; not wired in compose)
* Responsive / mobile layouts (**later**)
* React / a second SPA
* Pixel-clone of Motion Recruitment’s wordmark/photos, Apple, Toptal, Tesla, Manpower orange, or Robert Half

## Later

* Mobile / responsive pass (phone and tablet)
* Replace View as with session-only identity
* `grants` / permission codes
* Tesla-style full-bleed panels only if we choose a louder home later
