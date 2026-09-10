---
source: https://www.bullhorn.com/
updated: 2026-09-09
---

# Bullhorn

The category product: **ATS + CRM in one system** for staffing agencies, plus automation, search/match, and (in some markets) middle/back office (pay workers, onboarding). We are **building our own desk**, not integrating Bullhorn in v1.

## What they do

* One platform: clients, candidates, jobs, from prospect to placement.
* Recruitment CRM is three-way: **client ↔ job ↔ candidate** (generic Salesforce does this poorly).
* AI search/match, chat, automated sourcing (their Amplify). Data stays in their app.
* Marketplace + API for job boards, background checks, VMS.
* Middle office: paying contractors monthly (later-stage ops).
* Sold per seat to agencies (including very small teams).

## Ideas for Tekforce

| Idea | Status | Note |
| --- | --- | --- |
| ATS + CRM as one desk | **v1** | Locked |
| Three-way model: Account, Job, Candidate, Application | **v1** | Core schema |
| Search/match + score | **v1** | Existing evaluate module |
| Permissioned recruiter seats | **v1** | Configurable rights |
| Activity timeline on every record | **v1** | Thin: notes + status changes |
| Email/LinkedIn sync | later | Integrations |
| Job-board / background-check marketplace | later | Adapters, not a store |
| Middle office (pay contractors) | later | Same as RemotePeople Employ / billing |
| Sell this as SaaS to other agencies | later | Would need `tenant_id`; not the v1 business |

## Do not copy

Their AI brand, Salesforce packaging, or 10k-customer scope. Copy the **data model**: one system, three-way staffing relationships.
