---
name: xLatentStructure
description: >-
  Recover the constructs a codebase depends on but never declares — implicit state machines,
  required call orders, undeclared dict schemas, magic-string enums and fields that must change
  together — from every write and read of the value that carries each one. Emit one verified
  record per construct, with its sites, a diagram, each defect with a witness, and the explicit
  form, as a handoff for refactoring or bug-audit agents. Report only. Use when the user asks to
  find implicit or hidden state machines, protocols, schemas, enums or magic strings, asks what
  structure the code assumes but does not state, or wants a map of such constructs before a
  refactor. For defects of every kind use xLatentBugAudit; to land a cleanup use xSubsystemSweep.
user-invocable: true
argument-hint: <repo or subsystem>
effort: xhigh
---

# Latent structure

Find the structures that the code depends on but does not declare. Write one record per
structure, so that a different agent can act on it without reading the code again. Change
nothing.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: verification proves execution,
questions get answers not edits, the Bash style rule repeated in every subagent prompt and other
sessions share the tree.

## Terms

| Term | Meaning |
|---|---|
| construct | A structure that the behaviour depends on and that has no single declaration. It exists only as a pattern across the sites that use it. |
| carrier | The variable, field, dict key, literal or RAM address that holds the construct's value. |
| site | One write or one read of a carrier, at `path:line`. |
| guard | The condition that must be true for a write to run. |
| witness | The ordered sites, from an entry point, that reach a defect. |

## Kinds

| | Kind | Carrier | Example defect |
|---|---|---|---|
| K1 | state machine | status field, set of boolean flags, phase counter in a tick loop | writers can produce a flag combination that no reader handles |
| K2 | required call order | field set to null in the constructor and filled by a later method | a path reads the field before it is initialized |
| K3 | implicit schema | dict, JSON or kwargs keys | writer and reader spell a key differently, and a default hides it |
| K4 | implicit enum | literal compared at several sites; `isinstance` ladder; `type` field | one dispatcher misses a value and its default handles it silently |
| K5 | coupled fields | a cache and its source; a count and its list | one writer changes one field and not the other |

The checks for each kind and the record format are in `analyst-brief.md` beside this skill. When
you do not fan out, use the brief as your own checklist.

## Input

The scope. If the user named a subsystem, stay inside it. The report path is
`.claude/handoff/HANDOFF.LATENT-<SCOPE>.md`, scope in uppercase, unless the user names a different
path. That name lets `xHandoff read` consume it.

## Procedure

1. **Measure the scope.** Get `wc -l` per file, the language, and the entry points: `main`,
   handlers, tick or update functions, public API. Read the project `CLAUDE.md`. Record the
   commit hash. Each record is valid only at that commit.

2. **List the candidate carriers yourself, by grep.** One broad, cheap pass. Use
   `command grep -R` and self-test it on a planted hit.

   | Kind | Signal |
   |---|---|
   | K1 | a field named `state`, `status`, `mode`, `phase`, `stage` or `step` written in two or more functions; two or more boolean fields written in the same functions (`is_*`, `has_*`, `*_done`, `*_pending`); a counter changed every tick, with branches on its value; a `switch` or `match` on a field that its cases also write |
   | K2 | a field set to `None`, `nullptr` or `0` in the constructor and written in a different method; `if not self._x: raise`; methods named `init`, `setup`, `open`, `start`, `begin`, `close`, `reset` |
   | K3 | `x["literal"]` or `x.get("literal"` on one name in two or more functions; `**kwargs` passed down two or more levels; parsed JSON or YAML indexed directly |
   | K4 | one string or int literal compared with `==` or `case` in two or more files; an `isinstance` chain of three or more branches; a `type` or `kind` field compared with literals |
   | K5 | two fields written together in most functions and alone in one; `*_cache`, `cached_*`, `n_*`, `num_*` or `count` next to a collection |

   A construct has two or more values written at two or more sites, or two or more carriers that
   change together. Drop the other candidates. Rank the rest by sites × files.

3. **Recover the top candidate yourself, to a full record.** It becomes the exemplar in the
   brief, and it shows that the record format works on this code. Without it, analysts return
   lists of flags, not constructs.

4. **Group carriers, not files.** Put carriers that share sites in one group: a state field and
   the flags it gates, a dict and the enum key inside it. A construct crosses files. A file
   partition reports one state machine as three partial ones. Size each group so that one analyst
   can read every function that holds a site. Use six to ten analysts. If one reader can hold the
   scope, skip steps 4 and 5.

5. **Fan out with one brief.** Copy `analyst-brief.md` to the scratchpad. Fill in the scope, the
   exemplar record, the entry points and the project rules. Pass that one path to each analyst,
   with its group. Analysts are read-only and write their records to a scratchpad path that you
   name.

6. **Verify each record before it enters the report.** Run its recount command. Your count must
   be equal to the analyst's count. Trace each witness from its entry point. Where a test or a
   short script can run the witness, run it from the scratchpad and record the output. A defect
   without a traced witness goes in the unconfirmed list. A count that does not agree is the
   first finding.

7. **Merge.** Remove duplicate carriers that two groups reached. Link related records: a K4 enum
   that is the value set of a K1 machine, a K3 dict that carries a K1 status. Give each record
   its next consumer:

   | The record holds | Next |
   |---|---|
   | a defect with an executed witness | `xLatentBugAudit` plan entry, or a fix |
   | a defect with a traced witness that was not executed | `xHypothesisDebug` |
   | an explicit form that keeps behaviour | `xSubsystemSweep` wave |
   | an explicit form that changes behaviour | `xDesignDebate` ruling |
   | a K3 schema with silent defaults | `xConfigHygiene` |

8. **Write the report and stop.** No edits, no branches, no commits.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Partition by file | One state machine reported as three partial ones |
| Value set from the declaration | The enum declares five values; writers produce four, and a literal at one site produces a sixth |
| Transitions without guards | The diagram shows edges that cannot occur |
| Defect without a witness | "Can reach an invalid state", with no sequence of writes |
| Every boolean is a construct | Hundreds of records; the real machines are hidden among them |
| Dynamic access missed | `setattr`, `getattr`, `d[key_var]` and deserialization write a carrier where grep does not look; record its writers as open |
| `grep` honours `.gitignore` | `grep` can be an alias for a tool that skips ignored files; zero hits over files that match |
| Record without a commit | The consumer cannot tell a stale record from a wrong one |
| Fixing on the way | The report no longer matches the tree that the consumer reads |

## Report

Write the file from Input in this form:

```markdown
# HANDOFF.LATENT-<SCOPE>

Commit <hash>. Scope <paths>: <n> files, <LOC> lines. Entry points: <list>.

## State
| ID | Kind | Carrier | Sites | Files | Defects | Next |

## Records
<one block per record in the brief's format, most defects first>

## Open threads
LS<n> — <next skill> — <first concrete action>

## Verification
<the recount command of each record and its expected count; a different count means the record is stale>

## Unconfirmed
<defects without a traced witness>

## Refuted
<candidates that are not constructs, and why>

## Not read
<files outside every group; carriers with open writers>
```

In the reply, give the path, the State table, and the number of unconfirmed defects.
