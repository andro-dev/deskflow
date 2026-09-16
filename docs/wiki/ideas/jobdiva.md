---
source: https://www.jobdiva.com/
updated: 2026-09-16
---

# JobDiva

The other category product next to [Bullhorn](bullhorn.md): **front-to-back staffing ATS + CRM**, plus onboarding, VMS sync, and back office. Sold as PaaS/SaaS to agencies. Born inside a New York staffing firm ([Axelon](axelon.md)) in 2003 because off-the-shelf tools were not enough.

We are **building our own desk**, not buying JobDiva in v1. Use this page as a module map, not a shopping list.

## Business model

* Quote-based subscription to **staffing companies** (per seat / modules; they do not publish list prices).
* One proprietary stack: ATS, client CRM, job workflow, candidate careers portal, resume harvest from subscribed job boards, VMS spider/sync, timekeeping, billing, and (in some packages) VMS/MSP.
* White-label **candidate/hiring app** and **MyTime** timesheet app so the agency’s brand stays in front.
* Open API + 100+ integrations (job boards, background checks, payroll/GL).
* Regions: North America, UK, APAC, EMEA. UK/EEA data hosted in Oracle UK cloud (their FAQ).

They sell software. They do not run Tekforce’s placements.

## ATS + CRM (what they actually ship)

| Module | What it does |
| --- | --- |
| ATS | Req → search → submit. Resume harvest, suggested matches, patented search on **skill + duration of experience**. Email-to-ATS (`firm@jobdiva.com`) parses into the database in minutes. |
| CRM | Staffing-shaped client service: sales, account managers, and recruiters on one record. Mini-dashboards on every client. |
| Onboarding (middle office) | Paperless docs, e-sign, I-9 / E-Verify, background-check vendors, rules by client / locale / tax category. |
| DivaFinancials | Timesheets, approvals, billing, payroll handoff, contract **and SOW** jobs. Front-office activity flows into “true financials.” |
| VMS sync | Inbound reqs, timesheets, expenses, SOWs from major VMSs — they claim to have pioneered this. |
| Reports | 1000+ staffing reports; dashboards per role. |
| Portals / mobile | Agency-branded job search + apply; recruiter app; contractor time/expense. |

Search pitch (their FAQ): high **precision** (retrieved people actually have the skill for the required years) and high **recall** (you do not miss matches). Recruiter time shifts from reading resumes to interviewing and closing.

## Ideas for Tekforce

| Idea | Status | Note |
| --- | --- | --- |
| ATS + CRM as one desk | **v1** | Same lock as Bullhorn |
| Three-way Account / Job / Candidate | **v1** | Core schema |
| Search/match on skills + years | **v1** | Already in `score.py`; keep it explainable |
| Candidate careers site + apply | **v1** | Prototype already has this door |
| Activity / notes on records | **v1** | Thin timeline |
| Email-in resume parse | later | Ingest adapter; PII stays out of this public repo |
| Job-board harvest from **our** subscriptions | later | Legal harvest of accounts we pay for, not scraping |
| Onboarding packet + e-sign | later | Middle office |
| VMS inbound reqs | later | Needed when we join an MSP |
| Timesheets / billing / SOW financials | later | Employ + placements, not ATS columns |
| White-label candidate app | later | After the HTML portal is real |
| Recruiter productivity dashboards | later | After we have real volume |
| Sell Deskflow as multi-tenant SaaS | later | Needs `tenant_id`; not the v1 business |
| Job-board login harvesting / ToS-violating scrape | **never** | Even if their old FAQ describes a downloader |

## Why it matters

JobDiva is the proof that a **staffing firm can grow an ATS from its own desk** (see Axelon) and later sell that desk to others. Tekforce’s v1 is the Axelon chapter, not the JobDiva chapter: operate on our software. Keep module seams (ATS, CRM, match, portals, placements, later employ) so we do not have to buy this stack.

Their search idea is the one worth stealing in product language: **skill + years**, shortlist first, recruiter closes. That is Deskflow evaluate, not a chatbot.

## Do not copy

Their patents, harvester, VMS marketplace, or 40k-recruiter scale. Copy the **module split**: front office (ATS/CRM) → middle (onboard) → back (time/bill) as later packages, not one blob.
