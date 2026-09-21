# Safari adapter fork handoff

The `safari-adapter` branch is based on `browser-use/browser-harness` upstream
commit `afbcc381b963040c19627d788e40c7e7663171ee` (version 0.1.13).
It adds the existing Safari adapter as a separate package in `adapters/safari`.
The upstream source tree, package, skill, and installed tool remain unchanged.

The Safari runtime, bundled skill, smoke fixture and regression tests were copied
byte-for-byte from the verified implementation. Controlled live evidence follows
those source hashes; no new model-quality pass is claimed. See
[verification](adapters/safari/verification.md) for the exact scope and open gaps.

Published with the repository owner's explicit approval at
[tompulsarlabs/browser-harness](https://github.com/tompulsarlabs/browser-harness),
a public GitHub fork of `browser-use/browser-harness`. `safari-adapter` is the
default branch and local `origin`; `main` retains the upstream branch. The private
Safari repository remains the full archival source and a backup of this branch.

Implementation commit `78463db777b24174cbaf4b7f1e10a71c771200b8` is published.
[Public-fork CI run 34342126663](https://github.com/tompulsarlabs/browser-harness/actions/runs/34342126663)
passed all 27 Safari deterministic checks on that exact commit. No package release
was created. This publication bookkeeping changes no runtime.

Validation in this checkout passed: 15 Safari Python checks, 12 Safari Node checks,
266 upstream unit tests, and two optional upstream MCP tests after installing its
declared extra in the checkout's isolated environment. The first upstream run
skipped the MCP module; that gap was then checked explicitly. Wheel build, required
asset contents, source-byte equality, and an isolated wheel CLI invocation passed.
The upstream source, package metadata, skill and install guide have no diff.
See [import checks](adapters/safari/evals/results/import-checks.json).

No new Safari/Chrome browser or model-quality run was performed for the
unchanged-source import. Prior live results are preserved with source hashes.

## Upstream contribution

[Draft PR #781](https://github.com/browser-use/browser-harness/pull/781) targets
upstream `main` from `tompulsarlabs:contrib/safari-adapter`, commit
`87b62ff2578db9e0340aa69f766727bd1c595fb6`. The separate contribution worktree is
`browser-harness-contribution`; the fork's default branch remains `safari-adapter`.
The upstream diff is one focused commit with 13 files: adapter, tests, CI and
concise docs. Fork bookkeeping and archived logs stay outside the PR.

Runtime, bundled skill, fixtures, regression tests and package metadata are
byte-identical to the verified source. The contribution checkout passed 15 Safari
Python tests, 12 Node tests and all 268 upstream unit tests with the MCP extra.
[Fork CI run 34346406566](https://github.com/tompulsarlabs/browser-harness/actions/runs/34346406566)
passed on the exact contribution commit. Upstream GitGuardian and skill-review
checks passed; the PR was mergeable when submitted.

Keep the PR in draft for feedback on the optional-package approach and documented
target-identity limitations. No upstream merge was performed. Future PR changes
belong on `contrib/safari-adapter`, not the fork's default/bookkeeping branch.

## Privacy hardening — 2026-09-21

Tom authorized retaining the fork's browser/product-analysis capabilities and
shipping a security patch. Chrome harness usage analytics now require fresh
explicit content-free-v1 consent; legacy defaults do not enable sending.
The export boundary uses an allowlist for operation names, counts, lengths,
timings, outcomes and runtime metadata. Scripts, stdout content, form/helper
arguments, URLs, exception text and client/model environment strings are excluded.
Outbound analytics require HTTPS and do not follow redirects. Browser output
still reaches the calling agent. No new local page logs or recordings are added.

The Safari adapter and its separately installed private runtime are unchanged;
they have no telemetry sender. The fork now intentionally differs from upstream
in Chrome analytics policy. The upstream draft Safari PR is outside this patch.
Gstack is outside scope and unchanged. This does not solve the previously recorded
Safari document-identity/native-navigation limitations or sandbox arbitrary Python.

Deterministic checks: 285 harness unit tests (including 17 privacy regressions and
MCP tests), 15 Safari Python tests, 12 Safari Node tests; wheel build passed.
The original code failed 14 of the initial 15 privacy regressions. The baseline's
first missing-pytest attempt and Node's first incorrect working-directory attempt
were corrected, not counted as passes. [Case record](evals/privacy/2026-09-21.json)
contains source hashes and evidence limits. No new live-browser or model-quality
pass is claimed. Install a reviewed fork commit to retain these protections;
upstream PyPI reinstallation would replace them.

Shipped as [fork PR #1](https://github.com/tompulsarlabs/browser-harness/pull/1),
merged into `safari-adapter` at `d04d0531d1cb7862d9197314bd80a3f9eef8813b`.
Runtime commit `057c05d1ae850bbf87ad5b1472b0a6b738d85cdb` passed both
[branch CI](https://github.com/tompulsarlabs/browser-harness/actions/runs/35571945226)
and [PR CI](https://github.com/tompulsarlabs/browser-harness/actions/runs/35571972938).
The local uv Chrome tool now installs that exact Git commit with its MCP extra;
installed `run.py` and `telemetry.py` hashes match the tested source. Installed
CLI status reports `enabled: false`, policy `content-free-v1`, with no environment
override. Existing recording preference remains false. The standalone Safari
installation is unchanged. Local default checkout was fast-forwarded, preserving
pre-existing uncommitted files; contribution checkout and upstream draft PR were
not modified. No PyPI release was published.
