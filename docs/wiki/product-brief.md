---
updated: 2026-09-09
---

# Product brief

Tekforce LLC will use this system to grow a **multi-discipline** recruiting and staff-augmentation business (IT, CEO Search, medical, financial, legal, skilled trades, and more). v1 is a **simplified Robert Half**: public two-door site, logins, and an internal ATS + CRM.

The evaluate API already in this repo (fit score, evidence, draft note) becomes the **matching module** inside the ATS, not the whole product.

## v1 in one paragraph

A client drafts a job. An Exec or permitted Recruiter **approves** it. It appears on the public board. A candidate applies and tracks status. You run a **CRM** (companies, contacts, hire requests, notes) and an **ATS** (jobs, candidates, applications, stages, slates, fit score). Admin configures verticals, placement types, stages, and **who can see what**. Exec sees everything.

## In scope for v1

* Public marketing + job board + apply
* Candidate login (my applications)
* Client login (my jobs, my slates, hire request / draft job)
* Internal users: Admin, Exec, Recruiter
* Configurable verticals and placement types (DB or config, not hardcoded enums in UI only)
* Configurable permission grants (see [roles-and-permissions.md](roles-and-permissions.md))
* ATS pipeline + CRM accounts/contacts/activities
* Matching: reuse extract → score → note
* Placement record with fee/markup fields (no billing engine)

## Out of scope for v1

* Contractor timesheets, payroll, invoicing, Stripe
* Employer of Record / global payroll (RemotePeople Employ)
* FDM-style academy / employ-then-deploy
* RPO / MSP / VMS (Michael Page / Bullhorn middle office)
* 300-office footprint, salary-guide content mill
* Multi-tenant SaaS (selling this as Bullhorn). One company: Tekforce. Schema can grow a `tenant_id` later if you productize.

## Names

| Name | Meaning |
| --- | --- |
| Tekforce LLC | The operating company |
| Deskflow | This codebase and public GitHub repo |
| Hunt / Study | `job-os` and `learn-kb` — not this product |
