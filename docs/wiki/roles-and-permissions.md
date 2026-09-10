---
updated: 2026-09-09
---

# Roles and permissions

Access is **permission-driven**. Roles are default bundles. Admin can change grants. Exec is never locked out.

## Internal roles

| Role | Default bundle |
| --- | --- |
| **Admin** | Configuration: verticals, placement types, pipeline stages, permission templates, users. No desk work unless also granted ATS/CRM permissions. |
| **Exec** | All permissions. Cannot be denied by a template. |
| **Recruiter** | ATS (and CRM if granted). Scope can be limited by vertical, placement type, owner (book of business), and action (read / create / publish / submit slate). |

## Portal roles (not the desk)

| Role | Sees |
| --- | --- |
| **Candidate** | Public jobs, own profile, own applications, own status |
| **Client** | Own company jobs, own drafts, slates shared with them, hire requests |

Client and candidate are not Recruiters. Do not reuse the internal permission matrix for the public portal unless a grant is explicitly “portal:…”.

## Permission style (barebone)

Store grants as rows, not `if role == recruiter` in every endpoint.

```
principal (user or role template)
  → permission code (e.g. ats.job.publish, crm.account.read)
  → optional scope (vertical_id, owner_user_id, company_id)
```

Examples of codes to start with:

* `config.verticals.write`
* `config.permissions.write`
* `crm.account.read` / `.write`
* `ats.job.read` / `.create` / `.publish`
* `ats.candidate.read` / `.write`
* `ats.application.read` / `.move_stage`
* `ats.slate.send`
* `match.evaluate.run`

Every new feature adds a permission code. UI and API both check the same service.
