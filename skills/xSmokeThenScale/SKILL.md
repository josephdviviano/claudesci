---
name: xSmokeThenScale
description: >-
  Verify a training or pipeline change with a scaled-down local run, then hand it to the cluster
  as a pushed branch with launch instructions. Use when the user wants a smoke test before a
  real run, or says the full job cannot run on this machine.
user-invocable: true
argument-hint: <config, script or branch to smoke test>
---

# Smoke then scale

Prove the code path runs locally at small scale, then hand the real run to the cluster.

Follow `~/.claude/CONVENTIONS.md`, in particular: verification proves execution, no silent
fallbacks and per-repo policy is authoritative. Read `~/.claude/ENVIRONMENTS.md` for the current
cluster and job-submission facts — they are not repeated here because they drift.

## Input

The change to test, and the target scale it is meant to run at.

## Procedure

1. **Read the environment policy first.** The project `CLAUDE.md` gives the interpreter,
   environment manager and test runner (per-repo policy is authoritative).
   `~/.claude/ENVIRONMENTS.md` gives the cluster and submission mechanism. Using the wrong one
   produces failures that look like code defects.

2. **Scale down along the axes that do not change the code path:** steps, batch size, dataset
   size, model width, seeds. Do not scale down by disabling stages — a smoke test that skips the
   new stage tests nothing.

3. **Run it locally and confirm the new path executed** (verification proves execution). Not that the process exited
   zero: that the new code ran. A counter, a log line, or a changed output.

4. **Check the failure modes deliberately.** Does it crash on missing input rather than
   continuing (no silent fallbacks)? Are there silent defaults shadowing the config? Is the seed set?

5. **Confirm what the smoke test cannot tell you.** Small scale hides memory limits, distributed
   behaviour, data-loading throughput and convergence. Say which of these remain untested rather
   than implying the change is verified.

6. **Push the branch** and write the launch instructions: exact submission command, resource
   request, expected wall time, and where output lands. Absolute paths, no placeholders.

7. **Do not launch the expensive run yourself** unless asked, and do not commit or push beyond
   what the user requested (commit only when asked).

## Common mistakes

| Mistake | How it appears |
|---|---|
| Scaled down by disabling | The new stage is skipped and the smoke test passes vacuously |
| Exit zero read as success | The process ran, the new path did not |
| Wrong environment | A dependency error is diagnosed as a code bug |
| Heavy work on a login node | The job is killed, or the shared node is degraded |
| Smoke test presented as verification | Convergence and scale behaviour were never tested |
| Placeholder launch commands | The user edits paths by hand on the cluster, and gets one wrong |

## Report

What ran locally and at what scale, the evidence the new path executed, what remains untested,
the branch name, and the exact launch command.
