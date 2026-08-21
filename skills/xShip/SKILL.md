---
name: xShip
description: >-
  Close out work: review the diff, run the project's checks, commit, open a PR, resolve
  conflicts, and confirm nothing is left dangling. Use when the user asks to commit, push, open
  a PR, or wants everything merged with nothing left on the machine.
user-invocable: true
argument-hint: <branch or scope to ship>
---

# Ship

Land the work cleanly and leave the machine empty.

Follow `~/.claude/CONVENTIONS.md`, in particular: commit only when asked and per-repo policy is
authoritative. Read the project `CLAUDE.md` and `.pre-commit-config.yaml` for the project's
formatter and test policy — it differs per repository and using the wrong one wastes a CI cycle.

## Input

What to ship. If the user has not asked for a commit, push or PR, do not create one (commit only when asked).

## Procedure

1. **Read the diff before committing it.** You are the first reviewer. Anything in it you cannot
   explain does not belong in the commit — including changes you made while exploring.

2. **Apply the project's checks per its own policy** (per-repo policy is authoritative). Some repositories require the full
   formatter and test suite before a PR; others have no formatters and running them creates a
   large spurious diff. Read the project's configuration; do not assume.

3. **Work on a branch.** Never commit directly to the default branch. If work started there, move
   it to a branch first.

4. **Write minimal, neutral commit messages** (commit only when asked): what changed, not why, not how you
   arrived at it. Short enough to scan. No narrative, no provenance, no attribution trailers.

5. **Write the PR body at code level:** what the change does, in dense summary form for someone
   who has not followed the work. No narration of the process, no rationale essay, no
   attribution.

6. **Resolve conflicts by understanding both sides.** Never take one side wholesale to make the
   conflict disappear. Re-run the checks after resolving.

7. **Confirm nothing is dangling** before reporting done:

   | Check | What you are looking for |
   |---|---|
   | Uncommitted work | Modified or untracked files in this tree |
   | Other worktrees | Work in a sibling tree that never landed |
   | Unmerged branches | Local branches ahead of the remote |
   | Stashes | Anything parked and forgotten |
   | Open PRs | Earlier PRs from this line still unmerged |

8. **Do not merge unless asked.** The user merges.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Attribution trailers | Claude appears as co-author or as a participant on the PR |
| Narrative messages | The commit explains the journey instead of the change |
| Wrong formatter policy | A repository with no formatters gets reformatted, burying the real diff |
| Committing to the default branch | The collaborator's clean diff is gone |
| Exploration committed | Debug prints and scratch edits land with the change |
| "Done" with work elsewhere | A sibling worktree still holds the other half |

## Report

Branch, commits, PR link, checks run and their results, and the dangling-work table with every
row confirmed clear.
