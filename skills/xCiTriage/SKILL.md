---
name: xCiTriage
description: >-
  Root-cause one failing CI run and fix the cause, not the threshold. Use when a CI job fails,
  when a check passes locally but fails remotely, or when a test is flaky. For failures across
  many runs or cluster jobs, use xAnalyzeLogs.
user-invocable: true
argument-hint: <CI run URL or job name>
---

# CI triage

Find why this run failed, and fix that.

Follow `~/.claude/CONVENTIONS.md`, in particular: never edit the evidence, thresholds from measured or published data and per-repo policy is authoritative.

## Input

The failing run — URL, job name, or the log. Also which commit it ran against: CI often tests a
merge commit that exists nowhere locally.

## Procedure

1. **Read the failure itself, not the summary.** Find the first error, not the last line. Later
   output is usually cleanup noise from the first failure.

2. **Reproduce locally against the same commit** CI used. If CI tested a merge result, check that
   result out rather than your branch head.

3. **When it passes locally and fails remotely, compare the environments** before touching the
   code:

   | Compare | Typical cause |
   |---|---|
   | Tool versions | A linter or type checker version with new rules |
   | Interpreter | A different Python on `PATH` than the project's environment |
   | Dependency resolution | Unpinned transitive dependency moved |
   | Platform | Path handling, line endings, case sensitivity |
   | Available resources | Memory or core count differs from your machine |

4. **Pin the divergence** once found, in both places, so local and CI agree from now on.

5. **Never loosen a threshold, widen a tolerance, or add a retry to make a check pass** (never edit the evidence).
   That converts a visible failure into a silent one.

6. **Diagnose flakiness rather than re-running it.** A test that fails intermittently has a real
   cause — ordering, shared state, timing, an unseeded random source. Use `xHypothesisDebug`.
   Re-running until green hides it and it returns during a submission.

7. **Follow the project's own check policy** (per-repo policy is authoritative) when verifying the fix, and run the same
   checks CI runs.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Reading the last line | The reported error is cleanup from the real one further up |
| Testing the wrong commit | Local passes because CI tested a merge you do not have |
| Threshold loosened | Green CI, and the defect it detected is still present |
| Retry added | Flakiness is hidden until it appears at the worst moment |
| Version divergence unpinned | The same failure returns on the next contributor's machine |
| Fixing the test instead of the code | The assertion now matches the bug |

## Report

The failure, the first error and where, the root cause, the fix, what was pinned, and the
evidence CI now passes for the right reason.
