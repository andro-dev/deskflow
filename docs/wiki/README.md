# Tekforce / Deskflow project wiki

> A real staffing eBusiness for **Tekforce LLC**, starting as a simplified Robert Half.
>
> Deskflow is the product name in this repo. Tekforce is the company that will run it.

This wiki is the source of truth for **what we are building** and **ideas we might steal later**. The running code today is still the small evaluate API. Do not implement a wiki slice until a human says so.

## Table of contents

* [What we locked](#what-we-locked)
* [Wiki pages](#wiki-pages)
    * [Product](#product)
    * [Frontend](#frontend)
    * [Ideas from other companies](#ideas-from-other-companies)
    * [Architecture](#architecture)
    * [Tools](#tools)
* [How to add an idea](#how-to-add-an-idea)

## What we locked

* Public site like a **simplified Robert Half**: two doors (find a job / hire talent) **and logins**.
* First UI: [clickable prototype](frontend-prototype.md) for Andrew — full loop, Motion Recruitment look, My Tekforce login, SQLite users/roles. **Mobile later.**
* Candidates apply and track applications. Clients draft jobs and see slates.
* **You approve** a client job before it is public.
* Verticals and placement types are **data/config**, not code (IT, CEO Search, medical, financial, legal, trades, …; contract, CTH, permanent, executive search).
* Operator desk is **ATS + CRM**.
* Roles: **Admin** (configuration), **Exec** (everything), **Recruiter** (configurable ATS/CRM rights). Features are permissions. Portals for client and candidate stay small and separate.
* v1 records placements and agreed fees. Timesheets, invoices, and in-app payment come later.

Full write-up: [product-brief.md](product-brief.md).

## Wiki pages

### Product

* [Product brief](product-brief.md)
* [Roles and permissions](roles-and-permissions.md)

### Frontend

* [Frontend prototype](frontend-prototype.md) — clickable full loop; Motion Recruitment look; mobile later
* [Design references](ideas/design-references.md) — Motion v1 chrome; Apple / Toptal / Tesla watched

### Ideas from other companies

Track what they do, what we might adopt, and what we will not copy. Status on each idea: `watch` | `later` | `v1` | `never`.

* [Ideas index](ideas/README.md)
* [Robert Half](ideas/robert-half.md) — the v1 shape (two doors + recruiter in the middle)
* [RemotePeople](ideas/remotepeople.md) — **Recruit** and **Employ** menus (EOR / payroll)
* [FDM Group](ideas/fdm-group.md) — train, then deploy talent to clients
* [Bullhorn](ideas/bullhorn.md) — staffing ATS + CRM (+ middle office later)
* [Michael Page](ideas/michael-page.md) — perm / temp / executive / RPO-scale
* [Design references](ideas/design-references.md) — Motion Recruitment public chrome; Tesla watched
* [Backlog](ideas/backlog.md) — adopt / later / never

### Architecture

* [Barebone architecture](architecture.md) — modular monolith that can grow without a rewrite

### Tools

Engineering toolkit (MCP, test runners, runtime). Status is adopt/watch, not product features.

* [Tools evaluation](tools/README.md)
* [Chrome DevTools MCP](tools/chrome-mcp.md) — agent-driven Chrome for UI verify / debug (**watch**)

## How to add an idea

1. Open the company page or [backlog.md](ideas/backlog.md).
2. One idea per bullet: **source**, **what they do**, **what it would mean for Tekforce**, **status**.
3. Do not paste client or candidate PII here. This repo is public.
