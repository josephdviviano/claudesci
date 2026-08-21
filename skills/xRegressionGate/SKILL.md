---
name: xRegressionGate
description: >-
  Pin current correct behaviour as an executable artifact that later changes must reproduce, and
  enforce it. Use when protecting behaviour across a refactor, port or optimization, when
  setting up golden baselines or parity checks, or when staging a risky rewrite.
user-invocable: true
argument-hint: <behaviour to pin, or the rewrite to stage>
---

# Regression gate

Record what is correct now, executably, so a later change cannot alter it unnoticed.

Follow `~/.claude/CONVENTIONS.md`, in particular: never edit the evidence and thresholds from measured or published data.

## Input

The behaviour to protect, and the change it must survive. If the current behaviour is not known
to be correct, say so — pinning a defect makes it permanent.

## Procedure

1. **Record inputs and outputs, not summaries.** The artifact holds cases the system runs and the
   results it produced, so the comparison is executable rather than a judgement.

2. **Choose the comparison to match the computation:**

   | Computation | Comparison |
   |---|---|
   | Deterministic | Exact — bit-identical output or a hash of it |
   | Seeded but floating-point | Exact where the platform allows, otherwise a stated tolerance |
   | Stochastic | A distributional check over a fixed seed set, with the estimator stated |

3. **State the tolerance and where it came from** (thresholds from measured or published data). A tolerance chosen so the current
   code passes is not a tolerance, it is a rubber stamp.

4. **Make the gate cheap enough to run often.** If it is expensive, split it: a fast tier that
   runs on every change, and a heavy tier before merge or release. Say which is which, and what
   the fast tier does not cover.

5. **A failing gate is a test failure.** Never regenerate the artifact and never widen the
   tolerance to make it pass (never edit the evidence). Regenerate only for a deliberate, reviewed behaviour
   change, and record what changed and why it is correct.

6. **Stage risky rewrites as ordered steps,** running the gate at each one. The step that breaks
   the gate localizes the defect; a single large rewrite does not.

7. **Verify the gate can fail.** Perturb the code deliberately and confirm the gate catches it. A
   gate never observed failing may be comparing nothing.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Baseline regenerated to go green | The regression is now the recorded expectation |
| Tolerance widened | The check passes and no longer constrains anything |
| Gate never observed failing | It compares an empty set, or the wrong field |
| Only a heavy tier | Too slow to run, so it is skipped when it matters |
| Pinning unverified behaviour | A defect becomes the specification |
| Rewrite in one step | The gate fails and the cause is anywhere in the change |

## Report

What is pinned, where the artifact lives, the comparison and tolerance with its justification,
the tiers and their cost, and the evidence the gate fails when it should.
