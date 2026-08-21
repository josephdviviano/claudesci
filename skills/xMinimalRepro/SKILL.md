---
name: xMinimalRepro
description: >-
  Reduce a failure to a small case that provably preserves every condition the failure depends
  on. Use when a failure must be isolated, when a recorded result no longer reproduces, or when
  a reduced test disagrees with the real run. A reproduction that passes is not evidence until
  this check is done.
user-invocable: true
argument-hint: <failing case: run id, input, level, seed or command>
effort: high
---

# Minimal repro

Build a reduced case that fails for the same reason as the real one. A passing reduction proves
nothing until you have confirmed it preserves the conditions at the moment of failure.

Follow `~/.claude/CONVENTIONS.md`, in particular: verification proves execution, never edit the evidence and diagnostics must discriminate.

## Input

The exact failing case — run identifier, input, seed, level, or command — and the observed
failure. Keep the user's identifiers verbatim.

## Procedure

1. **Enumerate the conditions the failure could depend on, before you reduce anything.** Write
   the list down. Typical classes:

   | Class | Examples |
   |---|---|
   | Configuration | Flags, hyperparameters, feature toggles, tolerances |
   | State at the moment of failure | Active rules, cached values, accumulated state, mode |
   | Data identity | Split, version, preprocessing, ordering |
   | Multiplicity | How many items hit the mechanism at once, on one step |
   | Environment | Seed, device, backend, thread count, build flags |

2. **Capture those conditions from the real failing run, at the point of failure.** Step or replay
   to the point of interest and dump the state *there*. State read from the initial conditions is
   a different case: what a run starts with is often not what it fails with.

3. **Build the reduced case, and assert it matches the captured conditions field by field.** The
   assertion belongs inside the repro, so a later edit cannot silently change the case.

4. **Confirm the reduced case fails the same way.** Same symptom, same mechanism — not merely
   some failure.

5. **If the reduced case passes, the reduction dropped a load-bearing condition.** Return to
   step 1. Do not conclude that the reference data, the recording or the user's report is wrong.
   A passing repro built on the wrong conditions produces a confident, inverted verdict and an
   instruction not to look further, which is the most expensive failure mode this skill exists
   to prevent.

6. **Reduce further one condition at a time,** re-running after each removal. The case is minimal
   when removing any remaining condition makes the failure disappear.

7. **When code and reference data disagree, doubt the code first.** Settle it with the repro and
   never by editing the data (never edit the evidence). Bad data exists, but prove it — do not assume it because
   it is the cheaper conclusion.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Built from initial state | Conditions dumped at start, not at the failing step; the repro tests a different case |
| Surface preserved, substance dropped | Layout, names or shapes copied; active configuration or rules not |
| Multiplicity ignored | One item reproduces nothing because the bug is per-group, not per-item |
| "Verified in isolation" | True, and useless — the isolated path was never the failing path |
| Passing repro read as proof of bad data | The reduction was wrong, and the real defect survives |
| Assertions omitted | The repro drifts from the captured case and nobody notices |

## Report

State the failing case, the conditions you enumerated, which ones proved load-bearing, the
minimal case and where it lives, and the mechanism it isolates. If you concluded the reference
data is at fault, give the repro that proves it.
