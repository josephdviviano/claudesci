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

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: commit only when asked, per-repo
policy is authoritative and other sessions share the tree.
Read the project `CLAUDE.md` and `.pre-commit-config.yaml` for the project's formatter and test
policy — it differs per repository and using the wrong one wastes a CI cycle.

## Input

What to ship. If the user has not asked for a commit, push or PR, do not create one.

## Procedure

1. **Read the diff before committing it.** You are the first reviewer. Anything in it you cannot
   explain does not belong in the commit — including changes you made while exploring.

2. **Apply the project's checks per its own policy.** Some repositories require the full
   formatter and test suite before a PR; others have no formatters and running them creates a
   large spurious diff. Read the project's configuration; do not assume.

3. **Work on a branch.** Never commit directly to the default branch. If work started there, move
   it to a branch first.

4. **Write minimal, neutral commit messages**: what changed, not why, not how you
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

## Committing a subset of a shared dirty tree

When other sessions' work is interleaved with yours in one file, the commit is a subset of hunks.

- **Stage from `-U3` diffs. Never pair `git apply --cached` with `--unidiff-zero`.** A `-U0` hunk
  has no context, so git places it by line number alone and can apply it inside the wrong
  function. With context, a misplaced hunk fails loudly.
- **Test the staged patch, not the worktree.** Apply the exact staged patch to a `git archive` of
  `HEAD` in a scratch directory, build and test that, then stage. After the commit, compare its
  tree to the tested candidate (`git show HEAD:<f> | cmp - <candidate>/<f>`).
- **Carve fused hunks from a pristine checkpoint, not from the current text.** A sibling may have
  changed a helper you extracted. Your old call site against their new definition does not link.
- **Stage by positive identification of your own hunks, never by elimination.** Work you cannot
  attribute stays uncommitted, or is committed as explicitly unattributed — never under your own
  subject. "What is dirty" is not "what is mine": a sibling's tree-wide checkpoint commit can put
  its work in `HEAD` and leave several bodies of work dirty. `ListAgents` is a lower bound on who
  exists, because silence covers exited, busy and unregistered sessions. Run it again immediately
  before staging.
- **A green build says nothing about whose work is in the commit.** Content review and
  attribution review are separate checks.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Attribution trailers | Claude appears as co-author or as a participant on the PR |
| Narrative messages | The commit explains the journey instead of the change |
| Wrong formatter policy | A repository with no formatters gets reformatted, burying the real diff |
| Committing to the default branch | The collaborator's clean diff is gone |
| Exploration committed | Debug prints and scratch edits land with the change |
| "Done" with work elsewhere | A sibling worktree still holds the other half |
| Unclaimed work absorbed | The commit carries another session's work under your message |
| Worktree tested, commit not | The tree passes; the staged subset does not compile |

## Report

Branch, commits, PR link, checks run and their results, and the dangling-work table with every
row confirmed clear.
