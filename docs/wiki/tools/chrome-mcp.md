---
source: https://github.com/ChromeDevTools/chrome-devtools-mcp
docs: https://developer.chrome.com/docs/devtools/agents
npm: https://www.npmjs.com/package/chrome-devtools-mcp
updated: 2026-09-09
status: watch
---

# Chrome DevTools MCP

Google’s MCP server (`chrome-devtools-mcp`) gives a coding agent a live **Chrome** plus DevTools: click/type/navigate, screenshots, console, network, performance traces, Lighthouse.

Package: `chrome-devtools-mcp` (Apache-2.0). Cursor is a supported client.

## What it is for Deskflow

When the public site and portals exist, an agent should **exercise flows like a user**, not only run pytest:

* Candidate apply + “my applications”
* Client draft job → (you) approve → public board
* Recruiter desk: job, slate, permission-denied paths
* Responsive check (two-door homepage on desktop and a phone width)
* Catch console/network errors after a UI change

Until then it is useful for **competitor research** (Robert Half, RemotePeople, FDM, Bullhorn, Michael Page) without stuffing screenshots into git.

## How it compares

| Option | Strength | Weakness for us |
| --- | --- | --- |
| **Chrome DevTools MCP** | Real Chrome, Puppeteer waits, network/console, traces, Lighthouse, can attach to a running Chrome | Extra MCP process; Google usage stats on by default; exposes whatever is in that browser to the agent |
| **Cursor IDE browser** | Already in Cursor; CDP; good for “verify this screen” in-session | Cursor-owned tab, not your everyday Chrome profile; not the CI test suite |
| **Playwright in pytest** | Repeatable, reviewable, runs in GitHub Actions | Not an interactive agent loop; write tests after the flow is stable |

**Split we want:** Chrome MCP (or Cursor’s browser) for **agent-in-the-loop** while building. Playwright for **CI** once a flow is worth freezing. Do not replace pytest API tests with a browser MCP.

## Install (when we leave `watch`)

Cursor MCP config (user or project). Prefer pinning a version in the wiki when we actually turn it on; `@latest` is what Google documents:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest",
        "--no-usage-statistics"
      ]
    }
  }
}
```

`--no-usage-statistics` opts out of Google’s MCP telemetry (on by default). Official browsers: Google Chrome and Chrome for Testing.

Do **not** commit API keys or a logged-in Tekforce session into this repo. If we attach to a running Chrome (`--browser-url`), treat that profile as untrusted input: no real ATS with candidate PII.

## Risks

* Agent can see cookies and page content of the Chrome it controls. Use a throwaway profile for deskflow local UI and public competitor sites.
* Not a substitute for permission tests in the API (`access` module).
* Performance/CrUX calls can be disabled with `--no-performance-crux` if we do not want traces leaving the machine.

## Decision

**watch** — add to the toolkit when UI work starts (or sooner for competitor page walkthroughs). Revisit vs Cursor’s built-in browser after the first real portal slice; keep both if Chrome MCP’s network/Lighthouse tools earn their keep.
