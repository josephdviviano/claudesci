---
name: xSanitize
description: >-
  Remove a stated class of content from every surface of an artifact before it becomes visible
  where it cannot be retracted. Use for stripping identifying information before publication,
  anonymizing for double-blind submission, or removing unnecessary information.

user-invocable: true
argument-hint: <forbidden class> <artifact or repository>
effort: max
---

# Sanitize

Define what to remove, then remove it from every surface that carries it.

Follow `~/.claude/CONVENTIONS.md`, in particular: commit only when asked and bash style.

## Input

The forbidden class, stated precisely, and the artifact. If the class is vague, make it precise
with the user first: the scope of the sweep should be scaled such that the objective is fully satisfied,
using multiple passes for full verification.

## Procedure

1. **State the policy and the neutral replacement** before sweeping. What is forbidden,
   whether anything replaces it, and what is acceptable to keep. Write it down:
   the sweep will be repeated, and independent reviewers need the same definition you used.

2. **Enumerate the surfaces.** All must be checked:

   | Surface | Notes |
   |---|---|
   | Code and comments | These must be streamlined as much as possible to reduce surface area |
   | Symbol and file names | Code conventions must be satisfied at this level as well |
   | Config keys and test fixtures | Fixture data often holds extra information that should be removed |
   | Docs, README, papers | Including figures and their captions |
   | Generated artifacts | PDFs and images carry metadata which must be checked |
   | Commit messages and branch names | Visible on push, and permanent |
   | PR, issue and review text | Outside the repository, but equally crucial to be kept concise with no extra information |
   | History | Blobs of deleted files remain reachable |
   | Sibling worktrees and untracked files | Ship without being tracked |

3. **Sweep mechanically using predefined criteria** - this can be made systematic.

4. **Then review semantically.** Independent readers judge the text cold against the written
   policy. Regular expressions cannot catch paraphrase, and the author cannot audit their own.
   Include the bash style rules in every subagent prompt (bash style).

5. **Treat history as a separate, checklisted step.** If the policy reaches published history,
   rewriting requires a full backup first, a rewrite, and a force-push. Every recorded commit
   hash becomes stale afterwards — cite commits by subject line from then on. Do not begin this
   without explicit approval (commit only when asked).

6. **Verify after the sweep** with readers who did not perform it, against the same written
   policy.

7. **Install a check that stops the class returning** — a hook or CI step encoding the policy.
   Without it the sweep is repeated every few months.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Regular expressions only | Paraphrase survives, and the sweep is reported clean |
| Surfaces missed | Clean code, and the branch name or PR body is unchanged |
| Metadata ignored | The PDF is clean and its author field is not |
| Self-verified | The author reads past their own phrasing |
| History rewritten without backup | Irreversible, and something was lost |
| No returning check | The class is back within months - any finding should become a repeatable workflow |

## Report

The written policy, the surfaces swept and the findings per surface, what the independent review
found afterwards, whether history was rewritten and what that invalidated, and the check
installed to prevent recurrence.
