---
name: xDocSweep
description: >-
  Sweep a corpus of tracking docs — notes, plans, handoffs, TODOs — too large for one reader:
  correct stale claims against the code, settle conflicts, deduplicate, compact, and move each
  fact to one home in a layout agreed with the user, without losing an actionable item. Changes
  docs only, never code. Use when the user asks for a staleness pass, a doc cleanup or
  compaction, or says the tracking docs conflict, are out of date, or are too long.
user-invocable: true
argument-hint: <docs directory, e.g. .claude/>
effort: xhigh
---

# Doc sweep

Make a doc corpus true, short and easy for the next agent to use, and prove that no open item
was lost. `xDeslop` deletes what nothing references in a scope one reader can hold. `xWriteSte`
compresses one section. `xSpecDiff` checks one document against the code. `xHandoff` writes one
handoff. This sweeps the whole corpus and changes no code.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: verification proves execution,
questions get answers not edits, per-repo policy is authoritative, the Bash style rule repeated in
every subagent prompt and other sessions share the tree.

## Input

The docs directory. Read the project `CLAUDE.md` first: it may already name a doc layout, a
retirement rule, append-only records, a doc lint, or a rule for how docs are edited.

## Default layout

Recommend this layout, then agree the real one with the user (step 1).

| Kind | Home | Holds |
|---|---|---|
| Roadmap | `DESIGN_DOC.md` | What is built, and in which order |
| Durable knowledge | `notes/NOTES.<TOPIC>.md` | Facts true now, each with its evidence. No history |
| Unfinished campaign | `plans/PLAN.<TOPIC>.md`, `handoff/HANDOFF.<TOPIC>.md` | One entry point per open line of work: state, closed decisions, open threads with a next action, verification commands, traps |
| Open work | `tasks/TASKS.TODO.md`, `tasks/QUESTIONS.md` | Open items; an index at the top that maps each subsystem to its start doc, its verified state with a date, and what is owed. Open questions with their defaults |
| Records | `SESSION_LOGS.md`, `TASKS.DONE.md`, `NOTES.ABANDONED.md` | Append-only. Never revised |
| Superseded | `retired/` with a `README.md` | Where each retired doc's content went |

A closed campaign folds into NOTES, TODO and the log, and its plan or handoff retires.

## Procedure

1. **Agree the layout and the direction with the user before any work.** Show the default and
   the project's current layout side by side, and get a ruling on every difference. Then ask
   which plans are live and which are abandoned. Direction is not in the code; only the user
   knows it.

2. **Measure the corpus.** `wc -l` every doc. Give each doc its kind from the layout. Mark the
   records, generated data and `retired/` as do-not-touch. Find whether the docs are under
   version control: if not, a deletion cannot be undone.

3. **Take the inventory before any edit.** List every actionable item with its `file:line`:
   open TODOs, open questions and their defaults, open threads with their next action, rulings
   with their date and reason, constraints, traps, and verification commands. Store it as data
   in the scratchpad. This inventory is the regression check for the sweep: after each wave,
   every item has a new location, is closed with evidence, or is on the question list.
   Self-test it: remove one item from a scratch copy and confirm that the check catches it.

4. **Fan out read-only analysts.** Partition on doc families so that each analyst has a
   comparable line count. Copy `analyst-brief.md` beside this skill to the scratchpad, fill in
   the agreed layout, the project rules and the do-not-touch list, and pass that one path to
   every analyst. Each analyst returns its share of the inventory, a table of state claims, and
   findings in classes D1–D6. A corpus one reader can hold skips the fan-out; use the brief as
   your own checklist.

5. **Find cross-doc findings from the merged claims.** Group the claims tables by topic key.
   A topic with two values is a D2 conflict; a topic stated in several docs is a D3 duplicate.
   One analyst sees only its partition, so this step is yours.

6. **Verify each finding yourself before acting.** A stale claim needs the code, `git log -S`,
   or a test run that contradicts it. A closed item needs the commit or the result that closed
   it. Age is not evidence: an old doc can be correct, and a newer doc can be wrong.

7. **Split the findings three ways.** Information-preserving edits. Edits that need a ruling:
   every deletion or retirement, a conflict the code cannot settle, a plan whose direction is
   unknown, and anything that touches a record. And "verified but do not touch".

8. **Apply in waves, one doc family per wave.** Run `ListAgents` before the first wave and
   before each retirement. Use targeted edits, not whole-file rewrites. When a fact moves, update every reference to its old location (`command grep -rn`). Retire
   or delete only with the user's approval, and follow the project's rule for which. After each
   wave, run the inventory check and the project's doc lint if it has one.

9. **Stop on anything unexpected and return to the user.** An inventory item with no new
   location, a lint failure, or an edit that turns out to need a ruling. Do not resolve it and
   continue.

10. **Write for the next agent.** Each live doc opens with its scope and the date and commit it
    was verified against. State the present, not the history. Each open item has a next action.
    Point to a section by path and section name, not "see above".

## Common mistakes

| Mistake | How it appears |
|---|---|
| Inventory taken after the first edit | Nothing to check the result against; a lost TODO goes unnoticed |
| Stale judged by age | A correct old note is cut, or a wrong new one is trusted |
| Conflict settled by recency | The newer doc wins and was the one that was wrong |
| Open item compacted into a summary | Its next action, owner or default is lost |
| Record revised | `SESSION_LOGS.md` no longer says what happened |
| Deleted from an untracked directory | No history to recover it from |
| Fact moved, reference left | A doc points to a section that no longer holds it |
| Ruling stripped of its date or reason | The next agent re-opens a closed decision |
| Analysts editing | Every reported line number goes stale |
| Whole-file rewrite | An unreviewable diff that clobbers a sibling session's edit |

## Report

The agreed layout. A before/after scorecard: docs, lines, and inventory items (open count
unchanged unless items were closed with evidence). A move table — old location to new location
for every relocated fact, and where each retired doc's content went. Findings by class with the
evidence. The question list, each with a recommended default. Refuted hypotheses.
