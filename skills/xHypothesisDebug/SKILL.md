---
name: xHypothesisDebug
description: >-
  Find the cause of a defect by designing a measurement that discriminates between candidate
  causes, before any fix. Use when a bug's cause is not yet known, when a diagnosis must be
  proven rather than asserted, or when the user asks "why is this happening", "look into this",
  or "generate a hypothesis". Not for defects whose cause is already established.
user-invocable: true
argument-hint: <defect description, log path, or run command>
effort: high
---

# Hypothesis debug

Find a defect's cause by measurement that separates candidates. Fix only after the cause is proven.

Follow `~/.claude/CONVENTIONS.md`, in particular: verification proves execution, do not rationalize your instrumentation, diagnostics must discriminate and thresholds from measured or published data.

## Input

The symptom, and how it was produced. If the user gave a run command, a log, an object or run
identifier, or coordinates, keep them exact — they define the case you must reproduce.

## Procedure

1. **Restate the symptom as an observation.** Quote what was seen and the command or run that
   produced it. Do not name a cause yet. If the user proposed a cause, record it as one
   candidate among others, not as the conclusion.

2. **Enumerate candidate causes.** At least two, normally three to five. Each must be
   falsifiable — a candidate no measurement can rule out is not a candidate.

3. **Agree the list with the user before you instrument.** They will add candidates you cannot
   see from the code, and they will remove ones already excluded.

4. **For each pair of candidates, name the observation that separates them.** Write the
   prediction each candidate makes *before* measuring. If a proposed measurement is consistent
   with more than one candidate, it discriminates nothing — discard it and design another.

5. **Build the cheapest discriminating measurement.** Prefer reading state that already exists
   over adding instrumentation. Prefer per-item dumps over aggregates: an aggregate hides the
   one item that disagrees. If the measurement needs an automated or headless repro, use
   `xDebugHarness`. If it needs a reduced case, use `xMinimalRepro`.

6. **Run it and record the numbers.** Compare against the predictions from step 4.

7. **Eliminate candidates by evidence.** State which candidate each number rules out. If every
   candidate is eliminated, the enumeration was incomplete — return to step 2. If more than one
   survives, the measurement was not discriminating — return to step 4.

8. **Prove the surviving cause.** Show the mechanism in the code, and show that the path
   executes (verification proves execution). A cause that is merely consistent with the symptom is not proven.

9. **Fix the mechanism, not the symptom.** Report the fix before applying it if it changes a
   logic flow (a changed flow replaces the old one) or crosses into design.

10. **Verify with the measurement that discriminated,** and with the user's original
    reproduction. Both must change.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Gathering data instead of discriminating | Instrumentation is added, output grows, no candidate is ruled out |
| Confirming rather than separating | An observation consistent with two candidates is read as proof of one |
| Explaining your own number | An unexpected count is called "plausible" and kept; it was the bug |
| Threshold tuning | A constant is moved until the symptom stops. The cause is untouched and now hidden |
| Believing a stale artifact | The binary was not relinked, or the log predates the change |
| Fixing during diagnosis | Edits land while candidates are open, and the measurement no longer applies |
| Single-sample conclusions | One run stands in for a distribution (thresholds from measured or published data) |

## Report

One line each: symptom, candidates considered, the measurement chosen and what it separates,
the result, the proven cause, the fix, and how it was verified. State ruled-out candidates
explicitly — they stop the next session re-treading them.
