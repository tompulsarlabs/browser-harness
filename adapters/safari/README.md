# Safari Harness

An experimental Python CLI for controlling **normal Safari tabs** through macOS
Apple Events. It uses familiar browser-harness helper names without modifying the
upstream browser-harness installation. It is not a CDP compatibility layer.

## Status

Safari 26.6.2 passed three consecutive synthetic localhost runs covering page
reading, form entry, one click, separate CLI reuse, and a same-origin session marker.
The adapter remains experimental: same-URL tab replacement and native navigation
races are unresolved. See [fork handoff](../../HANDOFF.md) for evidence and pending work.

## Install

Requires macOS, Safari, Python 3.12, and uv. From the fork root:

```sh
uv tool install --python 3.12 --editable ./adapters/safari
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/safari-harness"
safari-harness skill > "${CODEX_HOME:-$HOME/.codex}/skills/safari-harness/SKILL.md"
safari-harness doctor
```

macOS may request Automation access to Safari. Page JavaScript additionally requires
**Allow JavaScript from Apple Events** in Safari's developer settings. The adapter
reports permission errors and does not modify these settings automatically.

## Use

```sh
safari-harness <<'PY'
tabs = list_tabs()
print(tabs)
# In a real task, select the intended tab by a unique known URL/title.
matches = [t for t in tabs if t['url'] == 'https://example.com/']
if len(matches) != 1:
    raise RuntimeError('Expected one matching tab')
switch_tab(matches[0])
print(page_info())
print(get_page_content())
PY
```

Helpers: `list_tabs`, `switch_tab`, `current_tab`, `page_info`, `new_tab`,
`goto_url`, `js`, `get_page_content`, `click`, `fill`, `scroll`.
`new_tab(url)` opens a **normal window** containing a tab; it can change focus.
Selection lasts for one CLI invocation. No automatic recording, screenshots,
page-content logs, or cloud service are used.
Failed `switch_tab()` or `new_tab()` calls clear the previous selection, including
invalid arguments. Select a fresh reference explicitly before another page action.

## Limits

- Safari exposes tab indices, not stable tab IDs. References include window ID,
  index, URL, and title; changed references and duplicate identical tabs in the same
  window are rejected. Re-list and select after navigation or a title change.
  Page JS also checks the exact URL immediately before evaluating the requested
  expression. This rejects modeled redirects to a different URL; it does not
  distinguish replacement documents with the same URL or guard native navigation.
  Concurrent user rearrangement can still race a command; do not use this prototype
  for consequential unattended actions.
- Navigation is asynchronous; verify the destination before acting. A successful
  navigation request is not proof that the destination loaded.
- Clicks and input events are synthetic. Sites requiring trusted input may reject
  them. `fill` supports inputs and textareas, not file inputs or contenteditable.
- No raw CDP, screenshots, recordings, trusted keyboard/mouse input, file upload,
  network interception, cross-origin iframe traversal, Promise results, or native
  dialog control. No promise of browser-harness script compatibility.
- Normal tabs use their Safari profile's browsing context. No cookies are copied or
  exported. Upstream browser-harness remains installed and unchanged.

## Checks

Run the following checks from `adapters/safari`:

```sh
uv run --python 3.12 python -m unittest discover -s tests -v
node --test tests/bridge.test.cjs
```

Node is only a test dependency. These deterministic tests mock Safari's scripting
objects and do not establish live browser or model quality.

The opt-in live check serves a synthetic page on loopback, opens one disposable
fixture window, and leaves it open. Its local server stops when the check exits.
It checks a separate CLI read, a synthetic session marker, selection-failure
recovery, exact textarea values, and a click counter. It rejects optimized Python
execution so assertions cannot silently disappear. Page JavaScript permission is
required. Fixture v3 completed three consecutive live runs on Safari 26.6.2. Its
reference check ignores window stacking order while still rejecting actual tab
reference changes.

```sh
uv run --python 3.12 python scripts/smoke_safari.py
```

[eval.md](eval.md) defines the acceptance criteria and bounded learning loop.
[evals/cases.md](evals/cases.md) maps those criteria to current test coverage.
[verification.md](verification.md) records verified behavior and unresolved target-identity findings.

Apple's own Safari MCP interface is available in Safari 27 beta / Technology Preview
247 and later, according to [WebKit's announcement](https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/).
This project targets the installed Safari 26.6.2 without requiring a beta upgrade.
