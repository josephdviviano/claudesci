---
name: xAutonomousCampaign
description: >-
  Execute a staged plan unattended, committing per stage and stopping at kill criteria. Use when
  the user asks for work to run autonomously, overnight, or through a plan or handoff without
  supervision.
user-invocable: true
argument-hint: <plan or handoff file to execute>
effort: high
---

# Autonomous campaign

Run a plan without a human present, and leave state the user can inspect and trust in the morning.

Follow `~/.claude/CONVENTIONS.md`, in particular: commit only when asked, questions get answers not edits and bash style.

## Input

The plan or handoff, and how far the user has authorized you to go. If the plan has no kill
criteria, add them and get agreement before starting (`xExperimentPlan`) — unattended work
without stopping conditions runs until it wastes the night.

## Procedure

1. **Confirm the authorized scope before starting.** Which stages, whether to commit, whether to
   push. Unattended work cannot ask, so anything ambiguous must be resolved now (questions get answers not edits).

2. **Verify the starting state.** Clean tree, correct branch, tests currently passing. Starting a
   campaign on a broken base makes every later failure ambiguous.

3. **Work stage by stage in the plan's order.** Commit after each completed stage so the user can
   review the sequence and revert one stage. Do not push unless asked (commit only when asked).

4. **Check the kill criterion at each stage boundary.** When one triggers, stop and record why.
   Stopping early with a clear reason is the successful outcome, not a failure.

5. **Verify each stage before moving on** (verification proves execution). A stage reported complete on an unexecuted
   path corrupts everything after it, and there is no one present to notice.

6. **Prefer headless and resource-aware execution.** No interactive tools, no dependence on a
   window. Consider that the machine may be on battery or shared.

7. **Include the bash style rules in every subagent prompt** (bash style). A permission prompt at
   two in the morning halts the campaign until morning.

8. **Do not expand scope.** Adjacent problems found on the way are recorded, not fixed (questions get answers not edits).

9. **End by writing a handoff** (`xHandoff`) with what was done, what stopped, and what is next.

## Common mistakes

| Mistake | How it appears |
|---|---|
| No kill criteria | The night is spent on a line of work that was dead by stage two |
| One commit at the end | The user cannot review or revert any single stage |
| Unverified stage completion | Later stages build on something that never ran |
| Pushed without asking | Unreviewed work appears on the remote |
| Scope expansion overnight | Morning diff contains changes nobody requested |
| Prompt-triggering commands | The campaign halts on the first permission request |

## Report

Stages completed with their commits, the stage that stopped the campaign and its criterion, what
was verified and how, findings recorded but not acted on, and the handoff path.
