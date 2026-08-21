---
name: xHandoff
description: >-
  Write or consume a handoff document that carries context between sessions, agents or machines.
  Use when the user asks for a handoff, a prompt for the next session, a spec for a cluster or
  collaborator agent, or asks to continue from an existing HANDOFF file.
user-invocable: true
argument-hint: write <TOPIC> | read <path>
---

# Handoff

Transport state between sessions. A handoff says what is true now and what to do next — never
what happened during the session.

Follow `~/.claude/CONVENTIONS.md`, in particular: verification proves execution, commit only when asked and stale docs get deleted.

## Input

Mode and topic. Files live at `.claude/HANDOFF.<TOPIC>.md`, topic uppercase, untracked unless
the project says otherwise.

## Procedure — writing

1. **Verify before you write.** Every claim of "done" must be checked by running something, not
   by recalling it (verification proves execution). A handoff that reports unverified state is worse than none: the
   next agent trusts it.
2. **State current state.** What works, what does not, and the evidence for each.
3. **Record closed decisions and why they are closed.** This is what stops the next session
   re-litigating them.
4. **List open threads, each with its specific next action.** No thread without an action.
5. **Give exact verification commands.** Runnable, absolute paths, no placeholders. The next
   agent runs these first.
6. **Record branch, PR and worktree state,** including anything uncommitted or unmerged.
7. **Name the traps.** Anything that cost time this session and will cost it again.
8. **Write durable facts to memory, not only to the handoff.** A fact that caused repeated
   confusion — a data split, a numbering scheme, an environment truth — belongs in project
   memory, where it survives the handoff being deleted.
9. **Keep it scannable.** Short sentences, tables over prose. If the reader cannot review it by
   eye, it is too long. No session narration.

## Procedure — consuming

1. Read the handoff, then **verify its claims before acting.** The repository moved after it was
   written, and other agents may have run against it.
2. Run the verification commands from the handoff first.
3. Report any discrepancy between the handoff and the repository to the user before continuing.
4. Do not treat the handoff as an instruction to commit or push (commit only when asked).

## Lifecycle

When a work line closes, fold the handoff's durable content into the design doc or notes and
delete the file (stale docs get deleted). A `DONE` handoff left in place is context pollution.

## Template

```markdown
# HANDOFF.<TOPIC>

## State
<what works, what does not, evidence for each>

## Decisions taken
<decision — why it is closed>

## Open threads
<thread — the next concrete action>

## Verification
<exact runnable commands>

## Git state
<branch, PR, worktrees, uncommitted or unmerged work>

## Traps
<what cost time and will again>
```

## Common mistakes

| Mistake | How it appears |
|---|---|
| Reporting unverified completion | "Wired up" written from memory; the path never executes |
| Narrating the session | A log of what was tried, instead of what is true now |
| Threads without actions | "Investigate lighting" with no next step |
| Placeholder commands | `<path>` or a relative path that fails from another directory |
| Facts only in the handoff | The handoff is deleted and the confusing fact returns next month |
| Stale handoffs left in place | Several DONE files, and the next agent follows the wrong one |

## Report

State the file written, the number of open threads it carries, and anything you could not
verify — one line each.
