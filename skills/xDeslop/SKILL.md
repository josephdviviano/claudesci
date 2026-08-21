---
name: xDeslop
description: >-
  Remove what nothing references: dead stages, placeholder branches, unrequested features,
  orphan config keys, and superseded docs. Use when the user asks for a de-slop pass, wants dead
  code or stale tracking docs purged, or suspects unrequested behaviour is in the pipeline.
user-invocable: true
argument-hint: <scope to purge>
effort: high
---

# Deslop

Delete what is not used, and everything that refers to it. Removes what nothing references —
`xAtomicConcepts` handles what is referenced but redundant.

Follow `~/.claude/CONVENTIONS.md`, in particular: verification proves execution, questions get answers not edits, stale docs get deleted and CLAUDE.md comment style.

## Input

The scope. The user often has a specific suspicion — a stage they think does nothing, a feature
they never asked for. Start there, then sweep the classes below.

## Procedure

1. **Enumerate candidates by class:**

   | Class | Where it hides |
   |---|---|
   | Placeholder stages | Named in the pipeline, implemented as a pass-through |
   | Dead branches | Conditions no configuration can satisfy |
   | Unrequested features | Optimizations and shortcuts nobody asked for (questions get answers not edits) |
   | Orphan config keys | Read by nothing, or read and ignored |
   | Superseded docs | Old handoffs, done TODOs, status files describing a previous design |
   | Stale comments | Describing code that has since changed (revise old comments) |

2. **Prove each candidate is dead** before removing it (verification proves execution). No call sites, no configuration
   path that reaches it, no test that exercises it, nothing in the history that suggests it is
   loaded dynamically. Absence of a direct call is not proof on its own.

3. **Treat unrequested behaviour as a finding, not just as clutter.** A quiet optimization or
   sampling shortcut in a results pipeline may have been corrupting results. Report what it did
   and for how long, and check whether any recorded result depends on it.

4. **Remove every reference, not only the definition** — call sites, config entries,
   documentation, paper text, tests, launch scripts. A removed stage still named in the paper is
   the same defect in a different file.

5. **Delete; do not archive** (stale docs get deleted). Commented-out code and `old/` directories are context
   pollution. History holds what was removed.

6. **Work in rounds, verifying after each,** rather than one large deletion. Run the project's
   tests between rounds.

7. **Keep comments that carry facts the code cannot** (CLAUDE.md comment style). Compressing comments is not the
   same as stripping them; do not remove a comment that records a constraint.

8. **List what you could not prove dead** for the user to decide, rather than deleting on
   suspicion.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Deleting reachable code | A dynamic or configured path breaks at run time, not at build |
| Archiving instead of deleting | `old_pipeline.py` survives and confuses the next reader |
| Definition removed, references left | Docs and configs still name a stage that no longer exists |
| Comments stripped wholesale | Constraints that were only recorded in comments are lost |
| One large pass | Something breaks and the cause is one of two hundred deletions |
| Unrequested feature quietly removed | Nobody learns which results it affected |

## Report

What was removed, by class, with the evidence each was dead. Separately: unrequested behaviour
found and what it affected, and the list you could not prove dead.
