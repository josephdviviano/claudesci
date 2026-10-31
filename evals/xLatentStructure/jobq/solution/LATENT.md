# HANDOFF.LATENT-JOBQ

Commit <fixture>. Scope `.`: 7 files, 143 lines. Entry points: `main.py:main`.

## State

| ID | Kind | Carrier | Sites | Files | Defects | Next |
|---|---|---|---|---|---|---|
| LS1 | K1 | `Job.running`, `Job.done`, `Job.failed` | 12 | 3 | 1 | xLatentBugAudit |
| LS2 | K4 | `Job.kind` | 6 | 5 | 1 | xLatentBugAudit |
| LS3 | K2 | `Store.path` | 6 | 3 | 1 | xLatentBugAudit |
| LS4 | K3 | `cfg` keys | 3 | 3 | 1 | xConfigHygiene |
| LS5 | K5 | `Queue.items`, `Queue.n_pending` | 10 | 2 | 1 | xLatentBugAudit |

## Records

### LS1 K1 Job.running / Job.done / Job.failed
- carrier: three booleans; declared at job.py:5-7; no state field
- recount: `command grep -nE '\.(running|done|failed)\b' *.py` → 12 lines
- values: written {queued, running, failed, done, running+failed, done+failed}; read {failed, done, running, queued}
- writers: job.py:5-7 → queued; scheduler.py:5 → running; scheduler.py:10-11 → done; scheduler.py:16-17 → failed; scheduler.py:22 → running [guard: attempts <= retries], failed not cleared
- readers: report.py:2-7 handles {failed, done, running, queued} in that order; running+failed → "failed"; done+failed → "failed"
- transitions: queued → running at scheduler.py:5; running → done at scheduler.py:10-11; running → failed at scheduler.py:16-17; failed → running+failed at scheduler.py:22; running+failed → done+failed at scheduler.py:10-11
- diagram:
  ```mermaid
  stateDiagram-v2
    [*] --> queued
    queued --> running: start
    running --> done: finish
    running --> failed: fail
    failed --> running_failed: retry (D1)
    running_failed --> done_failed: finish (D1)
  ```
- defects:
  - D1 A job that succeeds on retry is reported as failed. witness: main.py:35 → main.py:13 → main.py:18 → scheduler.py:17 → scheduler.py:22 → main.py:22 → scheduler.py:11 → report.py:2. result: default.log holds `b Evaluation failed: evaluated b`
- explicit form: `class State(Enum)` with one `job.state` field and a transition table; sites that change: 12; BEHAVIOUR CHANGE — job b is reported done
- related: LS4 — the retry guard reads the wrong cfg key

### LS2 K4 Job.kind
- carrier: string literal; no declaration
- recount: `command grep -nE '\.kind\b|"(train|eval|export)"' *.py` → 6 lines
- values: written {train, eval, export} at main.py:9; read {train, eval, export} at report.py:12, {train, eval} at runner.py:20
- readers: report.py:12 handles all three, KeyError otherwise; runner.py:26 handles {train, eval}; other values → run_train
- defects:
  - D2 An export job runs training. witness: main.py:35 → main.py:16 → runner.py:26. result: default.log holds `c Export done: trained c`; run_export (runner.py:16) has no caller
- explicit form: `class Kind(Enum)`; `HANDLERS` keyed by `Kind` with no default; sites that change: 6; BEHAVIOUR CHANGE — job c runs run_export

### LS3 K2 Store.path
- carrier: field set to None at store.py:3, written by `open` at store.py:6
- recount: `command grep -nE 'self\.path|store\.(open|save)' *.py` → 6 lines
- order: `open` must run before `save`
- defects:
  - D3 Per-job lines go to default.log. witness: main.py:35 → main.py:22 → scheduler.py:12 → store.py:9 runs before main.py:36. result: default.log holds the job lines; results.log holds only the summary
- explicit form: `Store(path)` takes the path in its constructor; delete the `or "default.log"` fallback; sites that change: 3; BEHAVIOUR CHANGE — job lines go to results.log

### LS4 K3 cfg keys
- carrier: dict from config.json, loaded at main.py:28
- recount: `command grep -nE 'retries|cfg\[|cfg\.get' *.py config.json` → 3 lines
- keys: written {max_retries, store}; read {retries, store}
- defects:
  - D4 The configured retry limit is ignored. witness: main.py:28 → main.py:19 → scheduler.py:21. result: `cfg.get("retries", 3)` returns 3; `max_retries` (2) is never read
- explicit form: `@dataclass Config(max_retries: int, store: str)` loaded without defaults; sites that change: 3; BEHAVIOUR CHANGE — at most 3 attempts, not 4
- related: LS1

### LS5 K5 Queue.items / Queue.n_pending
- carrier: two fields; declared at jobqueue.py:3-4
- recount: `command grep -nE 'n_pending|\.items\b' *.py` → 10 lines
- invariant: `n_pending == len(items)`
- writers: jobqueue.py:7-8 both; jobqueue.py:11-12 both; jobqueue.py:15 items only
- defects:
  - D5 The summary reports a pending job when the queue is empty. witness: main.py:33 → scheduler.py:29 → jobqueue.py:15 → main.py:37. result: results.log holds `summary pending=1`
- explicit form: delete `n_pending`; read `len(items)`; sites that change: 4; BEHAVIOUR CHANGE — summary reports pending=0

## Open threads

- LS1 — xLatentBugAudit — clear `failed` in retry, or replace the flags with one state field
- LS2 — xLatentBugAudit — register run_export; remove the run_train default
- LS3 — xLatentBugAudit — open the store before the loop
- LS4 — xConfigHygiene — read `cfg["max_retries"]` with no default
- LS5 — xLatentBugAudit — derive the count from `items`

## Verification

| Record | Command | Expected |
|---|---|---|
| LS1 | `command grep -nE '\.(running|done|failed)\b' *.py` | 12 |
| LS2 | `command grep -nE '\.kind\b|"(train|eval|export)"' *.py` | 6 |
| LS3 | `command grep -nE 'self\.path|store\.(open|save)' *.py` | 6 |
| LS4 | `command grep -nE 'retries|cfg\[|cfg\.get' *.py config.json` | 3 |
| LS5 | `command grep -nE 'n_pending|\.items\b' *.py` | 10 |

## Unconfirmed

None.

## Refuted

- `VERBOSE` (runner.py:3): one writer, one value set from argv; not a construct
- `label()` (report.py:12): handles every kind that is written

## Not read

None.
