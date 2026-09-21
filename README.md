<img src="https://raw.githubusercontent.com/browser-use/media/main/browser-harness/banner-ink.svg" alt="Browser Harness" width="100%" />

# Browser Harness ♞

Connect an LLM directly to your real browser through one editable CDP websocket. The agent writes missing helpers as it works, so the harness improves with every task.

Try browser-harness in [Browser Use Cloud](https://cloud.browser-use.com/v4?utm_campaign=browser-harness-use-in-cloud&utm_source=github) or paste the setup prompt into your coding agent.

```
  ● agent: wants to upload a file
  │
  ● agent-workspace/agent_helpers.py → helper missing
  │
  ● agent writes it                         agent_helpers.py
  │                                                       + custom helper
  ✓ file uploaded
```

**You will never use the browser again.**

## See it work

**Task:** "Open my X profile, find my latest 20 video posts, and download them."

[![Download my latest 20 X videos](docs/download-latest-20-x-videos.gif)](https://browser-use.com/showcase/videos/download-latest-20-x-videos.mp4)

## Setup prompt

Paste into Claude Code or Codex:

```text
Install or upgrade browser-harness to the latest stable version with uv using Python 3.12, register the skill from `browser-harness skill`, and connect it to my browser. Ask whether I want local browser recordings enabled; default to no and preserve my existing preference on upgrades. Follow https://github.com/browser-use/browser-harness/blob/main/install.md if setup or connection fails.
```

The agent will open `chrome://inspect/#remote-debugging`. On first setup, tick
the checkbox so the agent can connect to your browser:

<img src="docs/setup-remote-debugging.png" alt="Remote debugging setup" width="520" style="border-radius: 12px;" />

## How it works

- [`install.md`](install.md) connects the agent to your browser.
- [`SKILL.md`](SKILL.md) teaches it the browser workflow.
- [`src/browser_harness/`](src/browser_harness/) stays protected while the agent writes reusable helpers in its local workspace.

## Experimental Safari adapter

This fork includes an optional [Safari adapter](adapters/safari/README.md) for
existing Safari tabs through macOS Apple Events. It uses a separate `safari-harness`
CLI and package, with familiar helper names. Safari does not implement Chrome CDP;
the Safari runtime remains separate from the Chrome implementation.

The adapter has controlled live coverage for reading, form entry, clicking, and
session reuse. Same-URL tab replacement and native navigation races remain open;
see its [verification record](adapters/safari/verification.md).

## Privacy in this fork

Product inspection, page analysis, and browser automation stay available with
usage analytics disabled. Browser data returned to your agent is still subject
to that agent's own data-handling policy; the harness is not a Python sandbox.
Only run trusted scripts and authorize access to the intended tabs/accounts.

This fork's optional usage analytics are **off until explicitly enabled**:

```sh
browser-harness telemetry status
browser-harness telemetry enable   # opt in to content-free usage metrics
browser-harness telemetry disable
```

Opt-in sends operation names, counts, lengths, timings, outcomes, runtime versions,
and a random installation ID to Browser Use's EU PostHog project. It never sends
scripts, page output, URLs, selectors, form values, exception messages, custom
helper names, or model/client environment strings. Aggregate metrics remain
available for product usage analysis; raw content is not an analytics option.
The destination can be overridden with `BH_POSTHOG_HOST` (HTTPS only, no redirects).
`BH_TELEMETRY=0` overrides consent. Legacy configuration requires fresh opt-in.
The Safari adapter has no analytics sender and remains unchanged.

Install the reviewed fork commit rather than the upstream PyPI package to retain
this policy:

```sh
uv tool install --python 3.12 --force 'browser-harness[mcp] @ git+https://github.com/tompulsarlabs/browser-harness.git@<reviewed-commit>'
```

Do not use the upstream setup prompt above to reinstall this security fork.

## Scale with Browser Use Cloud

Use your local browser for logged-in, personal work. When you want many browsers in parallel—with live previews, proxies, stealth, CAPTCHA solving, and more—scale with [Browser Use Cloud](https://cloud.browser-use.com/new-api-key).

## MCP server

`browser-harness-mcp` exposes the browser control helpers as MCP tools over
stdio, so any MCP client (Claude Code, Devin, Cursor, etc.) can drive the
browser without writing a second CDP layer. See [docs/MCP.md](docs/MCP.md) for
setup and client configuration.

## Contributing

Bug fixes, documentation improvements, and agent-generated domain skills are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

[The Bitter Lesson of Agent Harnesses](https://browser-use.com/posts/bitter-lesson-agent-harnesses) · [Web Agents That Actually Learn](https://browser-use.com/posts/web-agents-that-actually-learn)
