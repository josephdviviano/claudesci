# Analyst brief — TEMPLATE

Copy to the scratchpad, fill in every section marked FILL, then pass the path to
every analyst.

# Doc sweep brief — <CORPUS>

You are ONE of N read-only analysts sweeping <CORPUS>. The orchestrator merges
every report and makes every edit. You edit NOTHING.

## Hard rules
- **READ ONLY.** Do not use Edit or Write on any doc or source file. Write your
  report to the path given in your scope.
- **Every finding needs evidence you checked.** A stale claim needs the code,
  `git log -S`, or a run that contradicts it. A closed item needs the commit or
  result that closed it. Age is not evidence.
- **Never propose a change to a record or a do-not-touch doc.** Read them as
  evidence only.
- **Never drop an actionable item.** A proposal that removes text lists every
  inventory item in that text and where it goes.

## Inventory — extract every actionable item in your docs

One row per item:

```
I-<n> | TODO|QUESTION|THREAD|RULING|CONSTRAINT|TRAP|COMMAND | path:line | <the item, verbatim, one line> | open | closed — <evidence>
```

A QUESTION keeps its default. A THREAD keeps its next action. A RULING keeps its
date and reason.

## Claims — state the docs assert about the project now

One row per claim about current state: a number, a default, a status, a
decision. These are what other docs may repeat or contradict.

```
<topic key> | <value> | path:line
```

Topic key: `<subsystem>.<thing>`, lower case, e.g. `audio.reverb.default`. Use
the same key for the same thing every time.

## Findings, in priority order

**D1 — stale claim.** The doc says one thing; the code, the git history or a
run says another. Give both values.

**D2 — conflict.** Two docs in your scope state values or decisions that cannot
both be true. Say which one the code supports, or that only the user can say.

**D3 — duplicate.** The same fact in several places. Propose the one home the
agreed layout gives it.

**D4 — closed.** A done TODO, a finished plan, a DONE handoff. List its durable
content — rulings, traps, facts — and the home for each, then propose
retirement.

**D5 — bloat.** Narrative, session history, debugging stories, repetition.
Propose the compressed text. Every fact in the old text appears in the new text
or in the move list.

**D6 — buried action.** An open item with no next action, or one held only in a
long doc and absent from the open-work doc.

## Reporting format

Write your report to the file named in your scope: first the inventory rows,
then the claims rows, then one block per finding, most severe first:

```
### <ID> <one-line claim>
- class: D1|D2|D3|D4|D5|D6
- sites: path:line[, path:line ...]
- evidence: what you checked (the grep, the commit, the run)
- inventory items affected: I-<n>, ... and where each goes
- proposal: the exact edit, precise enough to apply without re-reading the docs
- lines removed: <n>
- needs a ruling: no | yes — <the question, with a recommended default>
```

Finish with `## Summary`: counts of inventory items, claims and findings by
class, lines you would remove, and the three changes you would make first.
Return as your final message a digest: your scope, the counts, and the top three
findings. The orchestrator reads only that digest, so make it self-contained.

## Agreed layout
FILL: the layout agreed with the user, kind by kind.

## Do not touch
FILL: records, generated data, retired docs.

## Project rules that constrain proposals
FILL from the project CLAUDE.md: how docs are edited, the retirement rule, the
doc lint, the status vocabulary.

## Bash style
No `$()`, no `cd X &&`, no `VAR=` prefixes. Put helper scripts in the scratchpad.
`grep` may honour `.gitignore`; search docs with `command grep -rn`.
