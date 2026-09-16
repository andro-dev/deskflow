---
source: https://arc.dev/
updated: 2026-09-16
---

# Arc (arc.dev)

Remote talent **marketplace**: companies hire vetted freelance or full-time people (developers, designers, marketers, PMs, assistants) without running their own search. Not a traditional staffing desk, and **not** [ARCG](arcg.md) (`arcgonline.com`).

Grew out of Codementor (live mentorship, 2014) → CodementorX (remote developer hire, 2016) → Arc (2019). Codementor still sits in the footer as the sister product. Founder/CEO: Weiting Liu.

Closer to **Toptal** (gated network + matching) than to Robert Half (recruiter in the middle of every req).

## Business model

Public pricing is two SKUs; the homepage adds a third motion:

* **Freelance contracts** — talent sets an hourly rate (site quotes **$15–$110+**). Client pays hourly. Marketed SLA: hire in **72 hours**. Risk-free trial up to **two weeks**. Arc handles contracts and freelancer payments.
* **Full-time hires** — **20% of annual salary**, paid when you hire (“$0 until you hire”). Marketed SLA: **~14 days** vs a ~58-day traditional process. Three-month replacement: they match another person free of extra placement fee if it does not work.
* **Global teams** — dedicated recruiters, LATAM/APAC market entry, compliant hires via **trusted EOR partners** (Arc does not sell its own EOR the way [RemotePeople](remotepeople.md) does).

Talent joins **free**. Clients pay on hire. HireAI (screen inbound apps, auto-source and contact matches) is bundled on both paid plans. Full-time also lists ATS integration and a “20M+ candidates” worldwide pool.

Role families on the public site: developers, designers, marketers, product managers, project managers, assistants — plus country pages. Placement types they mention: freelance, full-time, part-time, contract-to-hire (CTH conversion has a fee).

## What they do (from the public site)

Two doors in the header: **For companies** (Hire talent) and **For talent** (Find jobs), plus Log In.

Company flow they publish:

1. Tell us needs (goals, budget, job details, location).
2. Meet top matches, already vetted.
3. Interview and hire; Arc handles freelancer pay and EOR partners.

Talent flow:

1. Create a profile.
2. Get vetted (communication +, for freelance, a domain interview).
3. Interview hiring managers directly.
4. Start work; talent partners still support.

Published vetting funnel ([How Arc works](https://arc.dev/how-arc-works)):

| Step | Filter | Claimed pass rate (of applicants) |
| --- | --- | --- |
| 1. Profile screening | Skills, training, experience | 55% |
| 2. Communication | English fluency, remote readiness (live or video intro) | 14% |
| 3. Technical / domain | ~1 hour expert interview or pair programming (role-specific: coding, campaign case, design challenge, PM roadmap) | **2%** (“top 2%”) |
| 4. Final review | Ongoing performance monitoring after they are in the network | Vetted |

Freelance needs both communication **and** domain interview. Full-time can be recommended after the communication test alone.

Content mill: freelance rate explorer, remote salary explorer, JD templates, interview questions — Codementor rate data under the hood.

## ATS / matching notes

The desk is not what they sell. Visible product is:

* A **pre-vetted pool**, then matching (HireAI + humans), then the client talks to talent.
* Dedicated recruiters as an add-on, not the default motion.
* Claims of 450k talent / 190 countries / 20M+ candidates / 800+ hires — treat as marketing.
* HireAI is marketed as instant shortlists and auto-outreach. Keep Tekforce scoring in `score.py`; do not replace it with an unbounded model score.

## Ideas for Tekforce

| Idea | Status | Note |
| --- | --- | --- |
| Two doors (companies / talent) + logins | **v1** | Same lock as Robert Half |
| Freelance / contract vs full-time as types | **v1** | Configurable; CTH already in the type list |
| Role families as public verticals | **v1** | Their row is tech-adjacent; ours stay config (IT, exec, medical, …) |
| Fit / slate so the client meets a shortlist, not a pile of resumes | **v1** | Existing evaluate module; they productized this as HireAI |
| Named shortlist SLA (e.g. 72h contract / 14d perm) | **watch** | Same class as RemotePeople’s “N in 72 hours”; operating capacity, not software |
| Pre-vet stages (comms + skills) before a candidate is submittable | **watch** | Named ATS stages; not a gated “top 2%” brand |
| Client talks to talent after a match (less recruiter in the middle) | **watch** | Marketplace motion. v1 stays recruiter-mediated; a later client portal already shows slates |
| Rate / salary explorer as content | later | Same bucket as Robert Half salary guides |
| Contractor payments / escrow | later | JobDiva DivaFinancials / timesheets; not v1 |
| EOR via partners for global hires | later | RemotePeople Employ; do not pretend we have Deel/Remote baked in |
| Dedicated recruiter / “global teams” SKU | later | Service line, not a module |
| Trial period / 90-day replacement as placement terms | later | Contract language on the placement record |
| HireAI-style auto-source and auto-outreach | later | Integrations; do not scrape boards |
| LATAM / APAC “market entry” as a product | later | Sales motion + EOR; not the desk |
| Elevate-style remote-job academy | later | FDM-lite training; needs ops |
| “Top 2%” / Silicon Valley-caliber funnel as a brand claim | **never** | Same as Toptal “top 3%” — we do not have that network |
| Claim 450k / 20M candidates we do not have | **never** | |
| HireAI as the fit number | **never** | Heuristic + optional extract only |
| Pixel-clone of black header + green CTA | **never** | Already locked Motion chrome; Toptal green is also never |

## Why it matters

Arc shows the **marketplace** version of remote staff aug: gate the supply (vetting), match fast, take a cut (hourly markup or 20% perm), and bolt on payments + EOR so the client does not run payroll in 190 countries.

Tekforce v1 is the **desk** version of the same two doors. Steal the **motion** (shortlist, types, later Employ), not the gated-network story. If we ever sell “you only meet people we already screened,” that is a named ATS stage plus Deskflow’s explainable score — not a second scorer and not a percentile slogan.

## Do not copy

“Top 2%,” HireAI copy, Codementor community size, wage-arbitrage as the homepage pitch, or their chrome. Copy the split: **find work / hire talent**, freelance vs perm economics, and Employ as a partnered later line.
