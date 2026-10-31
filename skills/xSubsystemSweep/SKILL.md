---
name: xSubsystemSweep
description: >-
  Sweep a subsystem too large for one context with parallel read-only analysts, hunting
  write-then-clobber defects, memory-safety and performance faults, duplicated authority, dead
  code, complexity, comment bloat and stale C++, then merge and apply the findings yourself in
  verified waves against a scorecard. Use when a subsystem hides bugs the size of a whole file,
  when the user says "there are probably many more of these", when one file runs to thousands
  of lines and a single reader cannot hold it, or when the user asks to clean up, refactor or
  modernize a system with no change in behaviour.
user-invocable: true
argument-hint: <subsystem or directory to sweep>
effort: xhigh
---

# Subsystem sweep

Partition a subsystem across parallel analysts, merge their findings, apply them yourself.
`xDeslop` removes what nothing references in a scope one reader can hold. `xLatentBugAudit`
hunts bugs and stops at a plan. This sweeps a subsystem too big for one context, hunts the
defect class that hides in size, and carries the result to landed edits. Cleanup is measured:
fewer lines, lower complexity, fewer comment lines, and no change in behaviour.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: verification proves execution, no
silent fallbacks, questions get answers not edits, the Bash style rule repeated in every subagent
prompt and other sessions share the tree.

## When this is the right shape

One file over ~5k lines, or one function over ~1k. At that size a value can be written with
intent at line 9100 and overwritten by an unconditional writer at line 9800, and no single
reading catches it. That is the target.

A system one reader can hold uses the same procedure without the fan-out: skip the partition in
step 2 and steps 3–4, and use the brief's taxonomy as your own checklist.

## Input

The subsystem, and — if you have one — a defect you just fixed or a refactor you just verified
inside it. The worked exemplar matters more than any description you can write. Prefer to find
one first.

## Procedure

1. **Find the exemplar before you fan out.** Make one real fix in the subsystem yourself: a bug,
   or a behaviour-preserving refactor that reproduces the baseline run. It calibrates every
   analyst and proves the class is live. Without it you get style opinions.

2. **Measure before partitioning.** `wc -l` the tree; list function boundaries. Record the
   scorecard: lines of code, comment lines, and cyclomatic complexity per function (`lizard`,
   or count decision points). The sweep reports against these numbers. Partition on
   real seams — one giant function split by line range, then file groups — so every analyst has
   comparable weight. Six to ten analysts.

3. **Write one brief, shared verbatim.** `analyst-brief.md` beside this skill is the template:
   copy it to the scratchpad, replace the subsystem name, the exemplar, the project rules and
   the build commands, and pass that one path to every analyst. For C++, copy `cpp-modern.md`
   beside it too. For other languages, delete C7 from the brief. The brief carries the priority-ordered taxonomy, the exemplar quoted in full,
   the reporting format, and the instruction to report cross-range findings anyway.

   | | class | why first |
   |---|---|---|
   | C1 | write-then-clobber | a value written with intent, overwritten before any read |
   | C2 | memory safety and performance | undefined behaviour and hot-path cost are not visible in the logic |
   | C3 | duplicated logic or constants | two sites WILL drift; one already has |
   | C4 | dead code | unreachable branches, fields with no reader, orphan diagnostics |
   | C5 | complexity | rank by cyclomatic and Halstead, propose named decompositions |
   | C6 | comment bloat | a comment that a name could replace, or narrative that belongs in NOTES |
   | C7 | stale C++ | an older idiom whose modern form removes lines or a defect class |

4. **Analysts are read-only on the repo.** They write reports to a scratchpad path you name.
   You apply every edit. This is not politeness — ten agents editing one file invalidates every
   line number in every report, including their own.

5. **Verify each headline claim yourself before acting.** Analysts over-state. Run the grep, read
   the ordering, count the writers. Several claims per sweep will be wrong, over-scoped, or true
   for a reason other than the one given.

6. **Split the merged findings three ways.** Behaviour-preserving. Behaviour-changing, which
   needs a ruling. And "verified but do not touch" — serialization vocabulary that looks dead,
   the other half of a documented A/B toggle, analysis tools for a campaign about to start.
   Many C2 fixes go in the second group: removing undefined behaviour or reordering float
   operations changes the output of a bit-exact baseline.

7. **Apply in waves, verify after each.** Build, run the suite, and re-run a deterministic
   scenario whose output you diff against the pre-sweep baseline. Tests check the cases someone
   wrote; the baseline run checks the whole output. The baseline diff is an oracle: validate it
   with `xRegressionGate` before the first wave. Commit a wave with `xShip`, which covers
   committing your hunks out of a tree that also holds other sessions' work.

8. **Stop on anything unexpected and return to the user.** A baseline-run diff, a test failure,
   a new build warning, or an edit that turns out to change behaviour. Do not diagnose and
   continue. Report the wave, its output, and the edits in it.

9. **Report refuted hypotheses.** An analyst that disproves something records it so nobody
   re-derives it. Carry those into the merged record.

## The exemplar, written for a brief

Quote your own, in this shape — the two sites, the ordering between them, and the observable
consequence. An illustration of the shape:

> `Pipeline.run` set `sample.weight = 0` for each sample below the quality cutoff at one point in
> the pass, and ~600 lines later an unconditional normalization loop wrote
> `sample.weight = raw[i] / total` for every sample. The normalization ran last, so the cutoff
> never took effect and rejected samples entered training. One 3000-line function; both writes
> inside it.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Fanning out before one real fix | Analysts return style opinions, not defects |
| Modernizing for its own sake | A C7 rewrite that removes no line and no defect class is a style opinion |
| Applying a C2 fix as cleanup | Removing undefined behaviour changes the output of a bit-exact baseline |
| Continuing past a baseline diff | The next wave hides the edit that caused it |
| Letting analysts edit | Ten agents in one file; every reported line number goes stale |
| Trusting a digest | A crude grep counted local variables as functions |
| Scanning a gitignored dir with the shell `grep` | `grep` can be an alias for a tool that honours `.gitignore`; zero hits over files that match — use `command grep -R` and self-test on a planted hit |
| Deleting serialization vocabulary | An enum with no writer still parses an older file on disk |
| Deleting the other half of an A/B toggle | Unreachable in the shipped config is not unreachable |
| Deleting the tools for the next campaign | Graph analysis with no caller, wanted next week |
| Gating log lines in bulk | A regex without an exclusion also silences a warning that must never be silenced |
| One large apply | Something breaks and the cause is one of two hundred edits |
| Claiming a wiring works because it built | A path can be reached every frame and still never exercised |

## Report

Findings by class with counts and LOC. The scorecard before and after: lines, comment lines,
and CC of the worst functions. The defects fixed, each with the evidence. The three-way
split, naming what needs a ruling and what you deliberately left. The baseline-run diff. What
remains, in the order you would do it.
