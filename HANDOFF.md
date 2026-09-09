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
passed all 27 Safari deterministic checks on that exact commit. No upstream PR
or package release was created. This publication bookkeeping changes no runtime.

Validation in this checkout passed: 15 Safari Python checks, 12 Safari Node checks,
266 upstream unit tests, and two optional upstream MCP tests after installing its
declared extra in the checkout's isolated environment. The first upstream run
skipped the MCP module; that gap was then checked explicitly. Wheel build, required
asset contents, source-byte equality, and an isolated wheel CLI invocation passed.
The upstream source, package metadata, skill and install guide have no diff.
See [import checks](adapters/safari/evals/results/import-checks.json).

No new Safari/Chrome browser or model-quality run was performed for the
unchanged-source import. Prior live results are preserved with source hashes.
