---
name: xRegressionGate
description: >-
  Pin current correct behaviour as an executable artifact that later changes must reproduce, and
  enforce it. Use when protecting behaviour across a refactor, port or optimization, when
  setting up golden baselines or parity checks, or when staging a risky rewrite.
user-invocable: true
argument-hint: <behaviour to pin, or the rewrite to stage>
effort: xhigh
---

# Regression gate

Record what is correct now, executably, so a later change cannot alter it unnoticed.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: never edit the evidence and
thresholds from measured or published data.

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
   | Seeded but floating-point | Exact where the platform allows, otherwise a tolerance from step 3 |
   | Stochastic | A two-sample test, or a confidence interval on the difference, over a fixed seed set. State the test, the seed count and the false-positive rate |
   | Timed or load-dependent | Not an oracle. Compare only what is invariant by construction: deterministic output, counts that must be zero, a semantic check of the defect class the change could reintroduce |

3. **Measure the noise floor, then set the tolerance from it.** Run the unchanged code N times,
   N stated, and record the spread of each compared quantity. Set the tolerance from that
   distribution at a stated false-positive rate. For example, a new run of unchanged code falls
   outside the range of N known-good runs with probability 2/(N+1), so N = 39 gives 5%. With
   several compared quantities the rates add up: state the rate for the whole gate. A tolerance
   below the noise floor reports false regressions. A tolerance chosen so the current code passes
   is not a tolerance, it is a rubber stamp.

4. **Make the gate cheap enough to run often.** If it is expensive, split it: a fast tier that
   runs on every change, and a heavy tier before merge or release. Say which is which, and what
   the fast tier does not cover.

5. **A failing gate is a test failure.** Never regenerate the artifact and never widen the
   tolerance to make it pass. Regenerate only for a deliberate, reviewed behaviour
   change, and record what changed and why it is correct.

6. **Stage risky rewrites as ordered steps,** running the gate at each one. The step that breaks
   the gate localizes the defect; a single large rewrite does not.

7. **Verify the gate in both directions.** Run it on known-good runs: it must pass them at the
   rate step 3 predicts. If it fails a clean build, the gate is wrong, not the code — change what
   it compares, and do not widen the tolerance until one run passes. Then perturb the code
   deliberately and confirm the gate catches it. A gate never observed failing may be comparing
   nothing.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Baseline regenerated to go green | The regression is now the recorded expectation |
| Tolerance widened | The check passes and no longer constrains anything |
| Gate never observed failing | It compares an empty set, or the wrong field |
| Only a heavy tier | Too slow to run, so it is skipped when it matters |
| Pinning unverified behaviour | A defect becomes the specification |
| Rewrite in one step | The gate fails and the cause is anywhere in the change |
| Tolerance below the noise floor | Two runs of unchanged code differ, and the gate reports a regression |
| Timed counts as the oracle | Machine load shifts a count, and the gate fails a clean build |
| One rate per quantity, many quantities | Twenty checks at 5% each fail a clean build most of the time |

## Report

What is pinned, where the artifact lives, the comparison, the noise-floor measurement, the
tolerance and the gate's false-positive rate with their justification, the tiers and their cost,
and the evidence the gate passes known-good runs and fails when it should.
