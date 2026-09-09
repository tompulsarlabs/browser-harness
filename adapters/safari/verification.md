# Safari verification

The adapter is experimental. Exact-URL checks do not distinguish replacement
documents with the same URL/title or opaque origins sharing a URL. Native
navigation still has a validation-to-execution race. No full promotion pass is
claimed; the acceptance contract is [eval.md](eval.md).

## Deterministic checks

The package contains 15 Python tests and 12 Node bridge tests. They cover failed
selection invalidation, explicit recovery, serialization, unsupported CDP,
permission/timeout errors, metadata validation, and executable modeled URL races.
Mocks and Node VM results do not establish Safari's live event/reference semantics.
Fork-local results are recorded in [the handoff](../../HANDOFF.md).

## Controlled live evidence

Fixture v3 passed three consecutive runs on Safari 26.6.2, Python 3.12.14, and
macOS 26.6.2. Each run checked:

- Exactly one new fixture window and unchanged pre-existing tab references.
- Load plus reuse by a separate CLI process within 30 seconds.
- An exact synthetic sessionStorage marker in the same Safari tab.
- Rejection after a stale selection or an invalid creation URL, then explicit recovery.
- Three exact textarea values containing Unicode, quotes, backslashes, newlines,
  HTML-shaped and shell-shaped text, followed by exactly one click and an exact read.

The runtime, skill, fixture, and regression files were imported byte-for-byte.
[Portable run records](evals/results/live-runs.json) include source hashes,
timestamps, commands, and original synthetic stdout. These are prior observed
runs against identical source, not new browser runs in the fork checkout.

Before fixture v3, one run passed and the next failed an ordered window-list
comparison. Instrumentation reproduced the failure with identical references by
window/index, zero changed URL/title fields, and zero added/missing references.
Fixture v3 compares references independently of window stacking order. Its tests
still reject actual tab moves, changed metadata, missing/added tabs, and duplicates.
The three v3 runs form a fresh sequence; the earlier failure is not counted as a pass.

## Remaining work

L3 live target-change/replacement coverage is absent. Multi-profile semantics,
file-fixture loading, native navigation races, and same-URL identity remain open.
D4–D7 retain coverage gaps listed in [the coverage map](evals/cases.md). Agent
behavior/model-quality evaluations have not run. No browser permissions, upstream
recording preferences, or installed upstream package were changed by this import.
