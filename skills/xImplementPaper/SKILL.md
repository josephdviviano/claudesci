---
name: xImplementPaper
description: >-
  Implement a paper's method inside an existing library, reproduce its headline result, and land
  it as a PR. Use when the user gives an arXiv link and asks to implement the method, or to
  reproduce a paper's results in their codebase.
user-invocable: true
argument-hint: <arXiv link or paper path>
effort: high
---

# Implement paper

Turn a paper into library code that reproduces the paper's own result.

Follow `~/.claude/CONVENTIONS.md`, in particular: a changed flow replaces the old one, commit only when asked and questions get answers not edits.

## Input

The paper, and which of its results are in scope. A paper has many claims; implementing all of
them is rarely what is wanted.

## Procedure

1. **Read the source, including the appendix.** Hyperparameters, initialization and the exact
   objective usually live there, and the difference between reproducing and not reproducing is
   usually there too.

2. **Extract the method as a specification** before writing code: objective, estimator, algorithm
   steps, hyperparameters with their values, and the reported result you are targeting.

3. **Agree the plan before implementing** (questions get answers not edits). Where the method belongs in the library,
   what it subclasses or reuses, and what existing code must change to accommodate it. Placement
   is a design decision the user will have opinions about.

4. **Reuse the library's existing machinery** rather than duplicating it. If an existing class
   needs an optional extension to serve the new method, extend it in a backward-compatible way
   rather than copying it — and remember that a changed flow replaces the old one.

5. **Work on a branch.** Implement the method, then the training script or example that exercises
   it.

6. **Reproduce the headline result** at whatever scale is available. Compare against the paper's
   reported numbers and state the gap. Where the full scale is not available locally, say what
   was run and what remains untested (`xSmokeThenScale`).

7. **Record every deviation from the paper,** with its justification. A deviation that is not
   written down becomes an unexplained discrepancy later.

8. **Write the explanatory notebook** where the user wants one: the method stated with its
   mathematics, its relationship to the methods already in the library, and a runnable example.

9. **Open the PR** when asked (commit only when asked), citing the paper in the code where a design decision
   comes from it.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Appendix skipped | The method is right and the hyperparameters are not, and it does not reproduce |
| Implemented beside the library | A parallel stack that shares nothing and diverges |
| Plan skipped | Placement is wrong and the review asks for a rewrite |
| Deviations unrecorded | A later session cannot tell a bug from a deliberate choice |
| Reproduction claimed from one run | A seed, reported as agreement with the paper |
| Scale difference unstated | Small-scale numbers are compared to paper-scale numbers |

## Report

What was implemented and where, the reproduction result against the paper's number with the
scale used, the deviations with justifications, and what remains untested.
