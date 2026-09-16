---
source: https://www.arcgonline.com/
updated: 2026-09-16
---

# American Recruiting & Consulting Group (ARCG)

Staffing and consulting brand: **find a job / find talent**, plus an hourly research product (Recruitment Intelligence™) and IT project delivery. Closer to a multi-line Robert Half than to a software vendor.

Not [Arc (arc.dev)](arc-dev.md), the remote talent marketplace.

## Business model

Four public service lines:

* **Recruitment** — contract, contract-to-hire, and permanent; retained and contingency.
* **Recruitment Intelligence™** — billed **hourly**, not as a placement fee. Client gets a pre-screened passive-candidate report sorted by **percentage match**, plus salary/benefits analytics. They **own the report** and can reuse it for later hires at no extra placement cost. Human recruiters stay on the search; RiC is their marketed AI assistant (matching, outreach drafts, 75+ job-board posts, fit grades).
* **Consulting** — specialists into client work (IT, finance, healthcare, executive, supply chain, HR, sales, admin, insurance).
* **IT Professional Services** — one person or a team for project work (app dev, data/analytics, PMO, managed services).

Revenue mix is classic staffing (markup / perm fee) **plus** hourly research **plus** project/consulting. Headquarters in Weston, FL; they list many U.S. city pages.

## What they do (from the public site)

* Two doors: **Candidates** and **Clients** (home CTAs: Find Your Dream Job / Find Talent Today).
* Practice areas as data, not one vertical: Technology & IT, Healthcare, Accounting & Finance, Executive Leadership, Supply Chain, Risk, Administration & HR, Sales & Marketing, Insurance, Legal.
* Published **7-stage recruiting process**: needs analysis → source passives → present + interview → debrief both sides → background check + final interview → offer/close → counter-offer coaching.
* Candidate login/register on the careers page; public login is **ARCway Careers** (RecruitOnline), not JobDiva or Bullhorn.

## ATS / matching notes

Their desk is not the product they sell. What is visible:

* Candidate portal + job search on the public site.
* Recruitment Intelligence scores candidates as a **% match** to the req and keeps “not ready now” people for later searches.
* Video “knockout question” interviews as a screening step before live time.
* RiC markets “beyond traditional ATS” sourcing (large profile graph, auto outreach, job-board blast). Treat those claims as marketing; keep Tekforce scoring in `score.py`.

## Ideas for Tekforce

| Idea | Status | Note |
| --- | --- | --- |
| Two doors + recruiter in the middle | **v1** | Same lock as Robert Half |
| Configurable verticals (IT, exec, healthcare, legal, …) | **v1** | Already locked |
| Contract / CTH / perm as placement types | **v1** | Already locked |
| Fit as an explainable % match on a slate | **v1** | Existing evaluate module |
| Named pipeline stages (needs → source → present → offer) | **watch** | Configurable stages already; their 7 steps are a good default template, including debrief and counter-offer |
| Hourly research / “you own the report” product | later | Different SKU from placement fee; needs packaging, not just software |
| Client reuses a slate for later reqs | later | Same candidate pool, new job; CRM + ATS already imply this |
| Video knockout-question screen | later | Portal feature, not v1 |
| Job-board blast + auto outreach | later | Integrations; do not scrape boards |
| IT project teams / managed services | later | FDM-shaped delivery, not the desk |
| RiC-style unbounded AI scoring | **never** | Heuristic + optional extract only |

## Why it matters

ARCG shows a **staffing firm that productized matching** (hourly, client-owned report) without becoming a SaaS vendor. Tekforce can keep placement fees as the v1 business and still leave room for a later “research retainer” SKU that reuses Deskflow’s score/evidence, not a second scorer.

## Do not copy

City-network claims, “billion profiles,” or RiC marketing. Copy the **motion**: two doors, named stages, % match the client can reuse.
