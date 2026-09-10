---
updated: 2026-09-09
---

# Tools evaluation

Possible tools for **building and operating** Deskflow / Tekforce. This is not the product feature backlog (that is [ideas/](../ideas/README.md)). Status here means “do we adopt this in the engineering toolkit?”

Status key: **in_use** · **watch** · **later** · **never**.

## How to add a tool

1. Add a row to the table below.
2. If the tool needs more than three lines, add `tools/<slug>.md` and link it.
3. Record: **what it is**, **what we would use it for**, **what we already have instead**, **status**, **risks** (PII, vendor lock-in, extra moving parts).

Do not paste secrets, MCP tokens, or real candidate/client data into these pages. This repo is public.

## Already decided (runtime)

Locked by the running MVP and [architecture.md](../architecture.md). Not up for a bake-off unless a human reopens them.

| Tool | Role | Status |
| --- | --- | --- |
| Python 3.11+ / FastAPI | HTTP API | **in_use** |
| pytest | API / unit tests (SDET proof) | **in_use** |
| Docker + GitHub Actions | Build and CI | **in_use** |
| AWS App Runner (from ECR) | Deploy path | **in_use** (docs; live URL later) |
| Postgres | Catalog, ATS, CRM, RBAC | **later** (when the modular monolith grows past evaluate) |

## Possible tools (evaluation)

| Tool | Kind | What we would use it for | Status | Page |
| --- | --- | --- | --- | --- |
| Chrome DevTools MCP (`chrome-devtools-mcp`) | Agent MCP | Drive a real Chrome: verify the two-door UI, debug network/console, Lighthouse, competitor research | **watch** | [chrome-mcp.md](chrome-mcp.md) |
| Cursor IDE browser (`cursor-ide-browser`) | Agent MCP (built-in) | Same class of “agent clicks the UI,” inside Cursor’s tab, no extra install | **in_use** when a browser is available in the session | — |
| Playwright | Test library (CI) | Repeatable E2E against candidate/client/desk flows | **later** (when there is a UI to test) | — |

Chrome MCP is **not** the product. It does not ship to candidates or clients. It is an agent-side browser so we can see what we built.
