---
name: xLatentBugAudit
description: >-
  Sweep a whole repository or subsystem for latent defects using scoped read-only auditors in
  parallel, and merge the results into one prioritized plan for human review. No fixes. Use when
  the user asks to find bugs across the codebase, or wants a plan of problems to review rather
  than changes.
user-invocable: true
argument-hint: <repo or subsystem to sweep>
effort: max
---

# Latent bug audit

Find defects across more code than one agent can hold, and hand back a plan, not a diff.

Follow `~/.claude/CONVENTIONS.md`, in particular: questions get answers not edits and bash style.

## Input

The scope to sweep. If the user named a subsystem, stay inside it.

## Procedure

1. **Partition the scope into disjoint file sets,** one per auditor. Size each set so an agent can
   read all of it. Overlapping sets waste effort and produce duplicate findings.

2. **Spawn one auditor per set, in parallel.** Every prompt states:

   | Clause | Why |
   |---|---|
   | Exactly which files are in scope | Prevents drift into another agent's set |
   | DO NOT MODIFY ANY FILE. Report only. | The deliverable is a plan (questions get answers not edits) |
   | What counts as a finding | Otherwise you get style opinions |
   | Evidence required: file, line, failing case | Unverifiable findings cost a round each |
   | The bash style rules | Rule 11, restated in every subagent prompt |

3. **Define what counts as a finding** before dispatch. Defects that change behaviour: wrong
   logic, unhandled state, silent fallbacks (no silent fallbacks), unreachable code (verification proves execution), assumptions the
   data violates, resource and lifetime errors. Not style, not naming, not preference.

4. **Merge and deduplicate** the returned findings. The same defect will arrive from several
   auditors under different descriptions.

5. **Verify before you promote.** Anything you cannot confirm from the code goes in a separate
   "unconfirmed" list, not into the plan. For high-stakes findings, have a second agent try to
   refute the finding rather than confirm it.

6. **Rank by consequence,** not by how interesting the defect is: what corrupts results first,
   what crashes second, what is merely wrong third.

7. **Write the plan and stop.** No fixes, no branches, no commits.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Unscoped auditors | Agents wander the repo, overlap, and miss their assigned files |
| Missing DO-NOT-MODIFY clause | Edits appear in the working tree during an audit |
| Findings without evidence | A list of suspicions the user must investigate themselves |
| No deduplication | One defect reported five times, ranked five times |
| Style findings | The real defects are buried under naming opinions |
| Fixing the easy ones on the way | The plan no longer matches the tree the user reviews |

## Report

The prioritized plan: each finding with file, line, the failure it causes, and its consequence
rank. Then the unconfirmed list, kept separate. State the partition you used and any files that
fell outside it, so the user knows what was not read.
