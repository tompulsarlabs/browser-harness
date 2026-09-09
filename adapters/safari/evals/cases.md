# Evaluation coverage

[eval.md](../eval.md) is the unchanged acceptance contract. This map distinguishes
implemented checks from the full promotion gate.

| Criterion | Evidence | Remaining gap |
| --- | --- | --- |
| D1 | Python transport-double cases; three live stale-index/local-invalid-URL recovery checks | Live transport creation failures are not covered. |
| D2 | Node metadata/duplicate/closed-window checks | Same-URL/title replacement and inter-event tab identity remain unresolved. |
| D3 | Executable Node VM URL-race cases reject before caller-body execution | No live adversarial race verification; native navigation and same-URL identity are outside the guard. |
| D4 | Transport argv/shell tests and three live exact DOM corpus runs | No separate actual host-statement sentinel check. |
| D5 | Permission and timeout/no-retry tests | Invalid-response and later-action coverage incomplete. |
| D6 | Explicit CDP error test | Executable upload, Promise and unsupported-element cases incomplete. |
| D7 | No recorder in this package; synthetic output only | No before/after artifact and upstream-preference test. |
| L1–L2 | Fixture v3: three controlled passes with exact values, one click, reuse deadline and unchanged references | File-fixture loading remains unresolved. |
| L3 | No runner | Live replacement/race cases absent. |
| L4 | Three controlled same-tab synthetic session marker reads from a separate CLI | Multi-profile semantics unverified. |
| A1–A5 | Contract only | No scored agent/model-quality runs. |

See [verification.md](../verification.md) and
[portable live evidence](results/live-runs.json). Full promotion remains blocked
by unmet criteria; a passing suite must not be reported as universal browser safety.
