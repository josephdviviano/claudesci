---
name: xCleanBranch
description: >-
  Extract the smallest complete branch for one feature from work that holds more — committed,
  uncommitted and untracked — and prove the extracted branch keeps the feature's behaviour and
  results. Use when the user asks for a clean branch, a minimal feature branch, or to split one
  feature out of mixed work. To commit and open the PR, use xShip.
user-invocable: true
argument-hint: "[feature] [base branch]"
---

# Clean branch

The smallest branch that carries the whole feature, and nothing else.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: verification proves execution,
commit only when asked, per-repo policy is authoritative and other sessions share the tree.

## Input

The feature and the base. If the feature is not named, infer it from the conversation and state
the inference before you extract. The base is the user's choice, else the current PR's base, else
the default branch.

## Procedure

1. **Inventory the source changes:** commits on the branch, uncommitted edits and untracked files.
   Mark each hunk or file as feature, unrelated or unsure. Ask about the unsure ones.

2. **Extract in a separate worktree** (`git worktree add <path> -b <branch> <base>`), so the
   source branch and its working files stay untouched. Use a descriptive branch name unless one
   is given.

3. **Carry only what the feature needs end to end:** its code, integration, configuration and
   tests. Leave out unrelated refactors, formatting changes, experiments, debug output and
   speculative work.

4. **Simplify what you carry.** Clear names, simple control flow and the repository's existing
   patterns. No new abstractions. Remove comments that repeat the code; keep comments that state
   a constraint.

5. **Prove the branch still does the job.** Run the repository's required checks and the tests
   that cover the feature. Then run the result the feature exists for — the metric, the output,
   the benchmark — on the clean branch and on the source branch, and compare. A clean branch that
   passes its tests and changes the result has dropped a load-bearing hunk.

6. **Review the full diff against the base.** Every hunk belongs to the feature, and nothing the
   feature needs is missing.

7. **Do not commit, push or open a PR unless asked.** Use `xShip` for that.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Extracted in place | `checkout` and `stash` in the shared tree rewrite files another session is editing |
| Unrelated hunk carried | A refactor or formatting change rides along and buries the feature |
| Load-bearing hunk dropped | Tests pass, and the result the feature exists for has changed |
| Untracked files forgotten | A new module never reaches the branch, which fails on a fresh clone |
| Result not re-run | "Clean" is claimed from a build alone |
| Feature inferred silently | The branch holds the wrong feature |

## Report

Branch, base and worktree path. The hunks kept and omitted, with each unsure one and how it was
resolved. The checks run and their results. The feature's result on the source branch and on the
clean branch. Anything that could not be validated.
