---
name: xAutonomousCampaign
description: >-
  Execute a staged plan unattended, committing per stage and stopping at kill criteria. Use when
  the user asks for work to run autonomously, overnight, or through a plan or handoff without
  supervision.
user-invocable: true
argument-hint: <plan or handoff file to execute>
effort: xhigh
---

# Autonomous campaign

Run a plan without a human present, and leave state the user can inspect and trust in the morning.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: commit only when asked, questions
get answers not edits and bash style.

## Input

The plan or handoff, and how far the user has authorized you to go. If the plan has no kill
criteria, add them and get agreement before starting (`xExperimentPlan`) — unattended work
without stopping conditions runs until it wastes the night.

## Procedure

1. **Confirm the authorized scope and the budget before starting.** Which stages, whether to
   commit, whether to push, and the limits on wall time, compute and money. Exceeding the budget
   is a kill criterion like any other. Unattended work cannot ask, so anything ambiguous must be
   resolved now.

2. **Look for an earlier run.** Read the campaign handoff, `.claude/handoff/HANDOFF.<TOPIC>.md`.
   If an earlier run stopped part-way, resume after its last verified stage; do not start again.

3. **Verify the starting state.** Clean tree, correct branch, tests currently passing. Starting a
   campaign on a broken base makes every later failure ambiguous.

4. **Work stage by stage in the plan's order.** Commit after each completed stage so the user can
   review the sequence and revert one stage. Do not push unless asked.

5. **Record progress after each stage** in the campaign handoff: the stage, its commit, its
   verification result and the budget spent so far. A crash at stage five then costs stage five,
   not stages one to four.

6. **Check the kill criteria and the budget at each stage boundary.** When one triggers, stop and
   record why. Stopping early with a clear reason is the successful outcome, not a failure.

7. **Verify each stage before moving on.** A stage reported complete on an unexecuted path
   corrupts everything after it, and there is no one present to notice.

8. **Prefer headless and resource-aware execution.** No interactive tools, no dependence on a
   window. Consider that the machine may be on battery or shared.

9. **Include the bash style rules in every subagent prompt.** A permission prompt at two in the
   morning halts the campaign until morning.

10. **Do not expand scope.** Adjacent problems found on the way are recorded, not fixed.

11. **Finish the handoff** (`xHandoff`) with what was done, what stopped, and what is next.

## Common mistakes

| Mistake | How it appears |
|---|---|
| No kill criteria | The night is spent on a line of work that was dead by stage two |
| One commit at the end | The user cannot review or revert any single stage |
| Unverified stage completion | Later stages build on something that never ran |
| Pushed without asking | Unreviewed work appears on the remote |
| Scope expansion overnight | Morning diff contains changes nobody requested |
| Prompt-triggering commands | The campaign halts on the first permission request |
| No budget | The kill criteria trigger after the compute is gone |
| No progress record | A crash at stage five restarts the campaign from stage one |

## Report

Stages completed with their commits, the stage that stopped the campaign and its criterion, the
budget spent against its limit, what was verified and how, findings recorded but not acted on,
and the handoff path.
