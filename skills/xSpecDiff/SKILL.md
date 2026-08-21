---
name: xSpecDiff
description: >-
  Compare an implementation claim-by-claim against one named source of truth — a paper, a
  reference implementation, a design doc, or a collaborator's written spec — and emit a
  discrepancy table with file and line. No edits. Use when the user asks whether the code
  matches a document, or whether a change deviates from the reference.
user-invocable: true
argument-hint: <source of truth> <implementation path>
effort: max
---

# Spec diff

Check whether the code does what one named artifact says it does. Report differences; change
nothing, and give no opinion on whether the design is good — that is `xFreshEyes`.

Follow `~/.claude/CONVENTIONS.md`, in particular: verification proves execution and questions get answers not edits.

## Input

Two things, both named explicitly: the source of truth, and the implementation. If the user has
not said which document is authoritative, ask. A diff against the wrong reference is worse than
no diff.

## Procedure

1. **Extract the claims from the source of truth, one per row.** A claim is anything checkable:
   a threshold, an equation, a stage ordering, a data split, a default, a reported count, a
   table entry. Quote each claim verbatim with its location in the document.

2. **Locate the implementation of each claim** and record file and line. A claim you cannot
   locate is itself a finding — either the behaviour is missing, or it lives somewhere the
   document does not suggest.

3. **Judge each claim** as one of:

   | Verdict | Meaning |
   |---|---|
   | matches | Code does what the document says |
   | differs | Code does something else — record both values |
   | missing | Document describes behaviour the code does not have |
   | undocumented | Code has behaviour the document does not mention |
   | unreachable | Code exists but never executes (verification proves execution) |

4. **Confirm reachability for anything you mark as matching.** Present in the file is not the
   same as running. Check the call sites.

5. **Do not resolve discrepancies yourself.** Which side is wrong is the user's decision: the
   document may need correcting as often as the code does.

6. **Change nothing** (questions get answers not edits).

## Common mistakes

| Mistake | How it appears |
|---|---|
| Comparing against the wrong version | The paper section was superseded, or the reference is an old commit |
| Paraphrasing claims | The quoted claim drifts and the comparison stops being checkable |
| Skipping tables and figures | Numbers in a table are claims, and are frequently the stale ones |
| Marking "matches" on presence | The code is there and never runs |
| Fixing the code to match | The document was the thing that was wrong |
| Reporting only differences | The user cannot tell what was checked and found consistent |

## Report

One table: claim, document location, implementation location, verdict, and both values where
they differ. Order by severity — differences that change results first, wording last. State the
source-of-truth version you compared against, so the diff can be repeated.
