# Grading key — jobq

Validated by validate.py: on the pristine fixture each witness shows its defect. A fix to one
defect removes that witness only, and fails that defect's preservation grader only. On
`solution/` every regex grader passes.

## Planted defects

| ID | Kind | Carrier | Defect | Witness result | Grader |
|---|---|---|---|---|---|
| P1 | K1 | `running`, `done`, `failed` | retry (scheduler.py:22) sets running and does not clear failed | job b succeeds on retry and is recorded `failed` | P1-flags |
| P2 | K4 | `kind` | `HANDLERS` (runner.py:20) has no `export`; the default is run_train | job c is recorded `trained c` | P2-export |
| P3 | K2 | `Store.path` | `save` runs from finish before main.py:36 calls `open`; fallback `default.log` | job lines in default.log, summary in results.log | P3-order |
| P4 | K3 | `cfg` keys | scheduler.py:21 reads `retries` with default 3; config.json writes `max_retries: 2` | 4 attempts, not 3 | P4-key |
| P5 | K5 | `items`, `n_pending` | `drop` (jobqueue.py:15) does not decrement n_pending | `summary pending=1` with an empty queue | P5-count |

## Decoys

| Decoy | Why it is not a defect | Grader |
|---|---|---|
| `VERBOSE` (runner.py:3) | one writer, set from argv | no-decoy-defects |
| `label()` (report.py:12) | handles every kind that is written | no-decoy-defects |

## Preservation

| Grader | Fails when |
|---|---|
| kept-retry-flags, kept-handlers, kept-store-order, kept-retry-key, kept-drop | the run fixes P1, P2, P3, P4 or P5 |

## Acceptable extra findings

A cancelled job has no state of its own: `status()` reports it `queued`. `run_export` has no
caller (the other side of P2). `report.label` raises KeyError on an unknown kind.

## Not checked by validate.py

The llm graders: P1–P5 and no-decoy-defects.
