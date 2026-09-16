---
source: https://www.axelon.com/search-jobs/
updated: 2026-09-16
---

# Axelon Services Corporation

Operating staffing firm that **built [JobDiva](jobdiva.md) for itself**, then kept running placements on that stack. Public slogan: **Staffing at the Speed of Insight**. Two doors (job seekers / clients) plus a JobDiva-powered job board.

Founded 1977 (earlier as Algomod). HQ 44 Wall Street, New York — same building as JobDiva. Woman-owned (Tania Obeid); JobDiva’s founder Diya Obeid came out of this desk.

## Business model

Client menu is broader than “we introduce you”:

* Business and technical **staff augmentation**
* Customized **project** solutions
* **Consulting**
* **Direct hire**
* **Workforce management** / contingent cycle (search → screen → submit)
* **MSP** partner (VMS programs, SLAs, dedicated teams)
* **Employer of Record / payroll**: on/off-boarding, employee care, workers’ comp & unemployment, benefits, PTO, talent community
* **RPO** (high-volume hiring, employer brand, cut agency spend)
* **Recruiter on demand** (their sourcers sit with the client team)

Placement types they advertise to seekers: permanent, freelance, contract, contract-to-hire.

Sectors (homepage): banking & financial services, telecom, pharma, insurance, food & beverage, energy, automotive, electronics, public sector, media, manufacturing, medical.

They sell **people and process**. The ATS is how they move faster than agencies that bought a generic CRM.

## ATS (publicly visible)

Axelon **uses JobDiva**, including for background-check tracking. The careers surface is a white-label JobDiva portal:

* [Search Jobs](https://www.axelon.com/search-jobs/) embeds `www1.jobdiva.com/portal/…` (iframe `jobdiva-portal`).
* Filters: keyword, country, state, city; **Create Job Alert**; tabs **all jobs** vs **My Ideal Jobs**.
* Job cards show title, **duration**, **shift**, **pay rate**, post date, and req id — contract-staffing UX, not a vague “apply somewhere.”
* Submit resume / apply goes to the same JobDiva portal signup.
* White-label **Axelon Services** mobile app (published by JobDiva Inc.): search/apply, track applications, store resumes, e-sign onboarding, assignment feedback.

Internal pitch: patented **“search skills by relevant years of experience,”** a large daily-refreshed database, and “never abandon a validated req until it is filled.” Client kickoff includes **KPIs** with the account manager.

## Ideas for Tekforce

| Idea | Status | Note |
| --- | --- | --- |
| Two doors + public Search Jobs | **v1** | Locked Robert Half shape |
| Perm / contract / CTH (and later freelance) as types | **v1** | Configurable |
| Job card with type, location, (later) rate/duration | **watch** | Useful for staff-aug boards; do not invent rates |
| Job alerts + “ideal jobs” | later | Candidate portal |
| White-label apply/onboarding app | later | After HTML portal |
| Staff aug + project + direct hire on one desk | **v1** | Types, not separate apps |
| KPI-based client kickoff | **watch** | CRM fields on the account; process, not a new module |
| MSP / VMS fulfillment | later | Same as Michael Page / JobDiva VMS |
| EOR / payroll / onboarding care | later | RemotePeople Employ |
| RPO | later | Process + contracts |
| Recruiter on demand | later | Staffing service, not software |
| Grow the ATS from our own desk (Axelon → JobDiva path) | **watch** | Strategy reminder: operate first, productize later |
| Claim a 30-million-person database we do not have | **never** | |

## Why it matters

Axelon is the **operating company** version of JobDiva. Tekforce looks like this: public board, recruiter desk, contract-heavy job cards, and (later) Employ. JobDiva is what happens if that desk is sold as SaaS. Keep those two stories separate in the wiki: we run Tekforce; we do not become an ATS vendor in v1.

Their search language matches Deskflow: **skills × years**, then a human submit. The public job board should stay a thin portal over **our** ATS, the way their iframe sits on JobDiva — not a second database.

## Do not copy

JobDiva branding, iframe, or “speed of insight” copy. Copy the **split**: marketing site + ATS-backed search, and keep EOR/RPO/MSP as named later lines.
