---
name: xExperimentPlan
description: >-
  Turn an agreed design into numbered milestones with cheap validation gating expensive compute,
  and an explicit kill criterion per stage. Use when the user asks for a roadmap, a linear plan,
  milestones, or how to sequence work before an expensive training run. Requires the design to
  be settled first — use xDesignDebate if it is not.
user-invocable: true
argument-hint: <the agreed design or goal>
---

# Experiment plan

Sequence work so the cheap result that would stop you arrives before the expensive one.

Follow `~/.claude/CONVENTIONS.md`, in particular: thresholds from measured or published data and questions get answers not edits.

## Input

The agreed design, and the compute available. If the design is still under discussion, stop:
planning an unsettled design produces a roadmap to the wrong place.

## Procedure

1. **Write the plan to a file** the user can edit, normally `.claude/PLAN.<TOPIC>.md`. The plan is
   the artifact; the conversation is not.

2. **Number the milestones linearly,** M0 upward. Each milestone states what it produces, and
   what must be true for it to count as done.

3. **Order by cost, cheapest first.** Synthetic before real. Small before large. Single seed
   before sweep. Local before cluster. The purpose of the ordering is to reach a decisive
   negative result before spending the compute.

4. **Give every milestone a kill criterion,** written before it runs: the observation that would
   make you stop or change direction. A milestone without one cannot fail, and so tests nothing.

5. **Put the gates in explicitly.** State which milestone must pass before the expensive one may
   start, and who decides. Gates the user must approve are marked as such.

6. **State what each milestone measures and how,** including the estimator and the spread. A
   milestone that produces a number nobody agreed to interpret produces an argument.

7. **Record the decisions the plan rests on,** so they are not re-litigated later. Link them, do
   not restate them.

8. **Do not start executing while writing the plan** (questions get answers not edits). The plan is reviewed first.

9. **Refresh the plan against the repository** before resuming it in a later session. Code moved;
   milestones may already be done, or no longer possible.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Expensive first | The big run finishes, and a cheap check would have predicted its failure |
| Missing kill criteria | Every result is interpreted as partial progress and nothing is ever stopped |
| Unstated gates | Someone launches the expensive stage because the cheap one "looked fine" |
| Milestones without acceptance | "Improve sampling" — done when? |
| Plan in the conversation | The next session cannot find it and re-derives it |
| Stale plan resumed | Milestones reference files and interfaces that have changed |

## Report

The plan file path, the milestone list with its gates, and the first kill criterion the user
will meet. Name anything the plan assumes that has not been verified.
