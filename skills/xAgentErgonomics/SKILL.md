---
name: xAgentErgonomics
description: >-
  Redesign a system's design documents and plans so that an agent operating it can orient,
  observe, act, verify and record with the fewest calls and tokens, measured by cold-start
  agents before and after the change. Use when the user asks to make a project
  agent-intuitive, agent-ergonomic, agent-accretive or legible to agents, asks how an agent
  would best drive or operate the system, asks you to put yourself in the driver's seat, or
  asks to rethink the project as one coherent system of linked abstractions. Edits documents
  and plans only; code changes become plan milestones. For one mechanism use xDesignDebate;
  for documents against code use xSpecDiff; for a staleness or compaction pass over tracking
  docs use xDocSweep.
user-invocable: true
argument-hint: <project, and its design documents and plans>
effort: max
---

# Agent ergonomics

Make the system easy for an agent to operate. Send agents with no context to do real operator
tasks. Redesign the documents and plans to remove what stopped them. Then measure again.
`xDocSweep` makes a doc corpus true and short. This skill finds what the operator needs from
the whole system, and redesigns the documents and plans to supply it.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: verification proves execution,
diagnostics must discriminate, no silent fallbacks, questions get answers not edits and the Bash
style rule repeated in every subagent prompt.

## Terms

| Term | Meaning |
|---|---|
| Operator | The agent that runs, inspects, changes and extends the system |
| Operator loop | Orient → observe → decide → act → verify → record. One pass per task |
| Agent-intuitive | The place an agent looks first for a thing is where the thing is |
| Agent-ergonomic | Each loop step costs few calls and little context, and its output decides the next step |
| Agent-accretive | Each session leaves its knowledge and tools in a fixed place, so the next session starts further ahead |
| Layer | A part of the system an agent can operate and verify from its contract, without reading the layers above it |
| Tower | The layers in dependency order, linked from one entry map |
| Battery | The set of concrete operator tasks, each with a true answer written before any agent runs |
| First wrong turn | The first file, name or command where a cold agent left the correct path |

## Input

The repository, its design documents and its plans. If the system is designed but not built, the
battery asks which command the agent would run and which output would decide the task. The
design is graded on whether it says.

## Procedure

Steps 1–6 change no file.

1. **Read everything before you judge anything.** Project `CLAUDE.md`, design documents, plans,
   entry points, configs, launch scripts, recent logs. For each document, record its path, its
   word count and what it owns. Run `git status` and `ListAgents`: documents are shared state,
   and another session may be editing one now.

2. **Take the operator's view: write the decision table.** List every decision the operator makes
   in the operator loop. For each, record the information it needs and how it gets it today:

   | Decision | Information needed | Command that gives it | Output size | Cost | Exists? |
   |---|---|---|---|---|---|

   A decision with no command is a gap. So is an output too large to read whole, and a cost the
   operator cannot know before it acts. Start from decisions, not components: a list of modules
   says what exists, not what the operator needs.

3. **Write the battery and its answer key.** One task per loop step, plus *extend* (add one new
   instance of the system's main extension point) and *diagnose* (find why a recorded run
   failed). Make each task concrete to this project. Add two held-out tasks. Write the true
   answer to every task before any agent runs.

4. **Run the cold start.** Use one fresh, read-only subagent per task. Brief each from
   `walkthrough-brief.md` beside this skill: copy it to the scratchpad, one copy per task. Run
   one task twice to measure the spread. Do not read the held-out reports until step 9. Grade
   the other reports against the key:

   | Grade | Meaning | Severity |
   |---|---|---|
   | Wrong | Sure, and incorrect: the documents mislead | Highest |
   | Stuck | Could not find what it needed | |
   | Guessed | Correct, but marked as a guess | |
   | Correct | Correct and sure | |

   Record per task: grade, tokens and duration from the completion notification, calls, first
   wrong turn, and where the agent looked first for each thing it did not find.

5. **Find causes, not symptoms.** The cause of a failure is its first wrong turn, not its final
   answer. Assign each failure and each decision-table gap to a loop step and to the property it
   breaks:

   | Property | Test |
   |---|---|
   | One name per concept | The same name in documents, code, config and logs |
   | One home per fact | Each fact is stated once; every other mention links to it |
   | Layering | Each layer's contract can be read whole; dependencies point down |
   | Bounded observation | Every state the operator decides on is readable in one call, as a table or JSON |
   | Explicit control | Every action is non-interactive, has explicit arguments, can be repeated, and has a dry run |
   | Cost before action | The time and compute of each action are stated; a cheap check gates each expensive one |
   | Findable results | A past result is found from its inputs (config, commit), not computed again |
   | Loud failure | A failure states what, where, and expected against received |
   | Fixed destinations | Each type of knowledge has one destination (table in step 6) |
   | Isolation | Parallel sessions cannot overwrite shared state: build directories, caches, golden files |

   Merge failures that share a cause. One cause, one fix.

6. **Design the tower.** Write, in this order:
   - The layers, bottom up. Each has its purpose in one line, its contract (inputs, outputs,
     invariants), its observe, act and verify commands, and the cost of each. They go in the
     design document, in place of any component list.
   - The entry map: the purpose in one sentence, the tower as a table of links, the two or three
     commands an operator runs first, and the destination table. It goes in the project
     `CLAUDE.md`, which every session loads. Every line there costs tokens in every session, so
     it holds links, not content.
   - The rename table, old name → new name, wherever documents, code, config or logs disagree.
     Until the code rename lands, the documents use the name the code uses.
   - The destination table. If the project already has an agreed doc layout (project
     `CLAUDE.md`, or from `xDocSweep`), use its homes; do not make a second layout. If not:

     | Knowledge | Destination |
     |---|---|
     | A decision and its reason | Design document decision log |
     | A trap that cost time | Project `CLAUDE.md` traps section |
     | A command sequence run more than twice | A script in one tools directory, one line in the map |
     | Behaviour verified correct | Regression gate |
     | Session state | Handoff, deleted when the work line closes |

   For each design choice, name the battery failure or decision-table gap it removes. Do not
   make a choice that removes none.

7. **Edit the documents in place.** Use Edit, not whole-file rewrites, so that concurrent edits
   survive. Mark every command as existing or `planned (Mn)`: a cold agent will try to run each
   command the documents present as real. Replace repeated facts with links to their home. List
   stale documents for the user to approve for deletion. Do not delete them.

8. **Edit the plans.** Each planned command, code rename and structural change becomes a
   milestone with an acceptance check, cheapest first, in the `xExperimentPlan` form. Write no
   code. Where a gap has a specialist procedure, name it in the milestone:

   | Gap | Skill |
   |---|---|
   | Silent defaults, divergent launch scripts | `xConfigHygiene` |
   | A manual loop to observe a defect | `xDebugHarness` |
   | No pinned baseline for correct behaviour | `xRegressionGate` |
   | Documents and code disagree | `xSpecDiff` |
   | Many implementations of one concept | `xAtomicConcepts` |
   | Dead stages, orphan keys, superseded documents | `xDeslop` |
   | Tracking docs that are stale, conflict, or repeat each other | `xDocSweep` |

9. **Measure again.** Use new fresh subagents with the same briefs and the same key, held-out
   tasks included. Grade changes are the primary result. A token change counts only if it is
   larger than the spread from step 4. If trained tasks improved and held-out tasks did not, the
   edits answer the battery instead of fixing structure: find the cause and do step 6 again for
   it. If orientation tokens increased, the map carries content instead of links.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Introspection in place of measurement | The redesign fixes what the builder thinks is hard; cold agents still get lost elsewhere |
| Generic advice | "Add a glossary", with no battery failure it removes |
| Components first | Documents list modules; the operator still cannot find what decides its next action |
| Legibility by addition | Documents grow, orientation tokens increase, grades do not change |
| Teaching to the test | Trained tasks improve, held-out tasks do not |
| Planned shown as existing | The operator runs a command that does not exist yet |
| Rename in documents only | Documents use the new name, code and logs the old one: now there are two |
| Unbounded status output | A status command that dumps the log; context fills before the decision |
| Implementing during the redesign | Code changes when the request was documents and plans |
| Whole-file rewrite of a shared document | Another session's edits disappear |

## Report

The decision table. The tower, one row per layer. The files edited and the milestones added. The
battery table: task, grade before and after, tokens before and after, held-out tasks marked.
Stale documents proposed for deletion. Decisions left for the user.
