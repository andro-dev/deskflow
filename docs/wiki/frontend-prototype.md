---
updated: 2026-09-09
---

# Frontend prototype

Clickable screens so **Andrew** can feel the product. Not a production UI, not login, not a database.

Implemented as HTML/CSS on FastAPI (`GET /`). The evaluate API is unchanged. In-memory sample data resets on process restart.

## Locked (interview 2026-09-09)

| Decision | Choice |
| --- | --- |
| Audience | Andrew (walk the loop himself) |
| Fidelity | Clickable screens, fake data, little or no login |
| Scope | **Full loop** in one prototype |
| Look | **Apple + Toptal blend** (see [design-references.md](ideas/design-references.md)) |
| Stack | HTML/CSS served by FastAPI |
| Auth | **View as** plus **My Tekforce** login (sample emails, no real passwords) |
| Brand on the site | Tekforce |
| Mobile | **later** — desktop first |

## Full loop (must click)

Public two doors → candidate applies → client drafts a job → exec/recruiter **approves** → recruiter sends a **slate**. Switch persona between steps.

Suggested pages (names can change):

1. Home (two doors: Find work / Hire talent)
2. Job board + job detail + apply (candidate)
3. My applications (candidate)
4. Draft job / hire request (client)
5. Approve queue (exec / recruiter)
6. Job + pipeline + send slate (recruiter)
7. My jobs / slate (client)
8. My Tekforce · Log in / Register / Forgot (Randstad-shaped portal door)

Sample names only (same policy as `samples/`). Verticals on the home page should *look* like config (IT, CEO Search, medical, …) even if they are hardcoded in HTML for this pass.

## Look

* **Public:** Apple restraint — thin nav, large type, lots of space. Toptal motion — two doors, specialties as a simple row, one primary action. No “top 3%” claims, no Toptal green clone.
* **Desk (approve / slate):** same type and spacing, quieter chrome, readable tables. Not a marketing hero.
* **Tesla.com:** looked at; **not** the home layout for this prototype. Notes on the [design references](ideas/design-references.md) page.

## Out of this prototype

* Real identity, hashed passwords, email verify, OAuth (Facebook/Google on Randstad stay **never** for this prototype)
* Sessions in Postgres
* Wiring `/v1/evaluate` into the slate (can show a **static** fit score on a sample candidate)
* Responsive / mobile layouts (**later**)
* React / a second SPA
* Pixel-clone of Apple, Toptal, Tesla, or Robert Half

## Later

* Mobile / responsive pass (phone and tablet)
* Replace View as with real identity
* Tesla-style full-bleed panels only if we choose a louder home later
