---
name: xAnalyzeLogs
description: >-
  Diagnose why runs failed or never started, across a body of logs. Use when the user asks why
  jobs failed, why runs are missing, or what happened to a sweep. Handles many runs at once —
  for one failing CI run use xCiTriage, and for plotting completed runs use xPlotResults.
user-invocable: true
argument-hint: <log directory, sweep name or job id range>
---

# Analyze logs

Say what was launched, what finished, and why each of the rest did not.

Follow `~/.claude/CONVENTIONS.md`, in particular: do not rationalize your instrumentation and bash style.

## Input

Where the logs are, and what was expected to run. If the expected set is unknown, reconstruct it
from the launch script or sweep config before reading any log.

## Procedure

1. **Build the expected set first.** Every configuration that should exist, from the sweep
   definition. Without it you can only describe failures you happened to find, and silent
   non-starts are invisible.

2. **Reconcile against what exists.** Three groups: completed, failed, and never started. The
   third is the one people miss, and it is often the largest.

3. **Fan out over the logs when the set is large.** One agent per directory or shard, each
   returning classifications rather than log text. Include the bash style rules in every subagent
   prompt (bash style), and require an example path per class so you can check the claim.

4. **Classify each failure by cause, from evidence in the log:**

   | Class | Signature |
   |---|---|
   | crash | Traceback or fatal signal; record the exception and site |
   | out of memory | Killer message, allocator failure, or host OOM |
   | preemption or timeout | Scheduler termination, wall-clock limit |
   | missing or bad input | File not found, wrong shape, wrong split |
   | silent non-start | Submitted and no log, or a log with no progress |
   | completed but wrong | Finished, and the output is empty or degenerate |

5. **Report counts per cause with an example path each.** A count you cannot open is not evidence.

6. **Explain anomalies rather than absorbing them** (do not rationalize your instrumentation). If nineteen of twenty runs crashed
   the same way and one did not, the outlier is the finding.

7. **Say which failures share a cause,** and which are independent. One fix often covers a whole
   class, and treating them separately wastes a cycle.

8. **Do not re-launch anything** unless asked (commit only when asked).

## Common mistakes

| Mistake | How it appears |
|---|---|
| No expected set | Only visible failures are counted; silent non-starts never surface |
| Reading logs into context | Thousands of lines consumed, conclusions no better |
| Cause guessed from the last line | The real exception was earlier, and the tail is cleanup noise |
| Counts without paths | The user cannot check any claim |
| Outlier absorbed | The one run that behaved differently is averaged away |
| Aggregating before diagnosing | Failed runs silently enter the results set |

## Report

Expected, completed, failed and never-started counts. Then the per-cause table with an example
path. Then which classes share a root cause, and what would have to change to recover the runs.
