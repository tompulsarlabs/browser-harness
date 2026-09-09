# Safari adapter fork handoff

The `safari-adapter` branch is based on `browser-use/browser-harness` upstream
commit `afbcc381b963040c19627d788e40c7e7663171ee` (version 0.1.13).
It adds the existing Safari adapter as a separate package in `adapters/safari`.
The upstream source tree, package, skill, and installed tool remain unchanged.

The Safari runtime, bundled skill, smoke fixture and regression tests were copied
byte-for-byte from the verified implementation. Controlled live evidence follows
those source hashes; no new model-quality pass is claimed. See
[verification](adapters/safari/verification.md) for the exact scope and open gaps.

Current preparation: fork-ready branch; public publication awaits the repository owner's
explicit public-visibility choice. GitHub requires a fork of public upstream to
be public. The pre-existing private Safari repository remains the full archival
source; this branch contains portable technical evidence and no personal session
handoff or account details.

Validation in this checkout passed: 15 Safari Python checks, 12 Safari Node checks,
266 upstream unit tests, and two optional upstream MCP tests after installing its
declared extra in the checkout's isolated environment. The first upstream run
skipped the MCP module; that gap was then checked explicitly. Wheel build, required
asset contents, source-byte equality, and an isolated wheel CLI invocation passed.
The upstream source, package metadata, skill and install guide have no diff.
See [import checks](adapters/safari/evals/results/import-checks.json).

No new Safari/Chrome browser or model-quality run was performed for the
unchanged-source import. Prior live results are preserved with source hashes.
