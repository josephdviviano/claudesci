# Analyst brief — TEMPLATE

Copy to the scratchpad, replace <SUBSYSTEM> and the exemplar in C1 with your own,
then pass the path to every analyst. If the exemplar is a refactor, put it under
its class and remove the C1 quote. The exemplar is not decoration: it is what
calibrates the sweep.

# Sweep brief — <SUBSYSTEM>

You are ONE of N read-only analysts sweeping <SUBSYSTEM>. The
orchestrator merges every report and applies the changes. You apply NOTHING.

## Hard rules
- **READ ONLY on the repository.** Do not use Edit or Write on any file under
  the repo. Write your report to the path given in your scope, which is in a
  scratchpad outside the repo.
- **Every claim must be verified before you report it.** Grep for readers of a
  field before calling it dead. Check write ordering inside the function before
  calling a write clobbered. A claim you could not verify does not go in the
  report.
- Do not report style preferences. A rename, a lambda or a modern idiom must
  remove a comment, a line, a decision point or a defect class.

## What we are hunting, in priority order

**C1 — write-then-clobber.** A value written, then overwritten before any read,
so the first write is dead and its intent is silently lost. This is the highest
priority category. The exemplar we just fixed, for calibration:

> FILL: the exemplar — the two sites, the ordering between them, and the
> observable consequence.

Look for the same shape everywhere: seed-then-overwrite, guard-then-restore,
two writers of one field in one pass, a field written on one thread and
re-derived on another.

**C2 — memory safety and performance.** Memory, C/C++: an owning raw pointer with no
clear owner, an index with no bound check, a pointer or reference into a
container that later grows, a read of an uninitialized member, signed overflow,
type punning through a cast, a field shared between threads with no
synchronization. Performance, only on paths that run every step, frame or
sample: a copy of a large object, an allocation, a repeated lookup of one key,
work that does not change between iterations. Give the call rate of the path as
evidence. Most memory fixes change behaviour; mark them BEHAVIOUR CHANGE.

**C3 — duplicated logic or duplicated constants.** The same predicate, the same
formula, or the same magic number derived independently at two or more sites.
Report every site. A threshold that exists in two places WILL drift.

**C4 — dead code.** Unreachable branches, fields nothing reads, statics nothing
consumes, diagnostics whose output no longer has a consumer, parameters always
passed the same value, `TEMPORARY`-marked scaffolding that outlived its purpose.

**C5 — complexity.** Rank the functions in your scope by cyclomatic complexity
and by Halstead volume/difficulty. For the worst offenders propose a concrete
decomposition: which contiguous block becomes which named helper, what it takes
and returns, and what the resulting CC is. Prefer extractions that also remove a
C1 or C3 finding. Give real numbers, not adjectives — count decision points and
operator/operand vocabulary yourself if no tool is available.

**C6 — comment bloat.** Comments carrying narrative, history, measurement
stories, tuning justification, dead ends, or references to how a bug was found.
A comment that explains a block is a name the code does not have: propose the
helper or variable name that replaces it. A formula keeps a comment only for
what names cannot carry: units, the derivation, a cited paper.
Project rule: code comments state WHAT the code does and the invariants a
future editor would otherwise break. Everything else belongs in a NOTES file.
Quantify: how many comment lines in your scope, how many you would cut.

**C7 — stale C++.** An older idiom whose modern form removes lines, a decision
point, or a defect class. Use the table in `cpp-modern.md` beside this brief.
Its third column is the condition under which the rewrite keeps behaviour; if
you cannot show the condition holds, mark the finding BEHAVIOUR CHANGE.

## Reporting format

Write your report to the file named in your scope. Use exactly this shape, one
block per finding, ordered most severe first:

```
### <ID> <one-line claim>
- category: C1|C2|C3|C4|C5|C6|C7
- sites: path:line[, path:line ...]
- evidence: what you checked that makes this certain (the grep you ran, the
  ordering you traced, the reader you failed to find)
- risk: behaviour-preserving | BEHAVIOUR CHANGE — <what observably changes>
- proposal: the concrete edit, precise enough to apply without re-deriving it
- lines removed: <n> (comment lines: <n>)
```

Finish the file with a `## Summary` section: total findings by category, total
LOC and comment lines you would remove, and the three changes you would make
first.

Then return, as your final message, a compact digest: your scope name, the
counts, and the top three findings with their IDs and one-line claims. The
orchestrator reads only that digest, so make it self-contained.

## Project rules that constrain proposals
Fill this section from the project CLAUDE.md before sending. It is what stops an
analyst proposing an edit the repo forbids. Typical entries: comment style, the
log-gating mechanism a diagnostic may already sit behind, which stderr lines must
never be silenceable, and where configuration is allowed to live.

## Build and test
Fill in the project's build and test commands. You may build to check a claim,
but do not leave the tree modified: read, do not write.

## Bash style
No `$()`, no `cd X &&`, no `VAR=` prefixes. Put helper scripts in the scratchpad.
