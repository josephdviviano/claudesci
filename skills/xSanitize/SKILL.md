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

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: commit only when asked and bash
style.

## Input

The forbidden class, stated precisely, and the artifact. If the class is vague, make it precise
with the user before you sweep. Plan more than one pass over the whole artifact: a mechanical
pass, a semantic pass, and an independent check after both.

## Procedure

1. **Write the policy down before sweeping.** What is forbidden, the neutral replacement if any,
   and what may stay. Save it as a file in the scratchpad: the sweep is repeated, and independent
   reviewers need the definition you used.

2. **Encode the policy as a pattern file** in the scratchpad, one extended regular expression per
   line. Self-test it: plant one forbidden string in a scratch copy and confirm the sweep reports
   it. A pattern set never seen to hit may match nothing.

3. **Sweep every surface mechanically,** and record the hit count per surface:

   | Surface | Where the class hides | Sweep |
   |---|---|---|
   | Tracked files: code, comments, config, fixtures, docs | Paths, names, hostnames, example values, data copied from a real run | `git grep -n -I -E -f <patterns>` |
   | File and directory names | Names derived from the class | `git ls-files \| command grep -E -f <patterns>` |
   | Figures and generated files | Pixels and captions; metadata such as author, creator tool and file paths | Read figures by eye; `exiftool <file>` |
   | Commit messages, authors, branch and tag names | Visible on push, and permanent | `git log --all --format='%an %ae %cn %ce %s %b'`, `git branch -a`, `git tag` |
   | History | Blobs of deleted or changed files stay reachable | `git log -p --all \| command grep -n -E -f <patterns>` |
   | PR, issue and review text | Outside the repository | `gh pr view <n> --comments`, `gh issue view <n> --comments` |
   | Untracked and ignored files, other worktrees | Ship without being tracked, or get added later | `git status --ignored`, `git worktree list`, then sweep each worktree |

4. **Strip metadata from generated files.** Where you can, regenerate the file from its source
   with the metadata fields empty. Otherwise strip it with `exiftool -all= -overwrite_original
   <file>`: without the flag, exiftool keeps a `_original` copy that still holds the metadata. On
   a PDF, exiftool appends an incremental update and the old metadata stays recoverable, so
   rewrite the file afterwards (for example `qpdf --linearize <in> <out>`) and read it again.

5. **Then review semantically.** Independent readers judge the text cold against the written
   policy. Regular expressions cannot catch paraphrase, and the author cannot audit their own.
   Include the bash style rules in every subagent prompt.

6. **Treat history as a separate, checklisted step.** If the policy reaches published history,
   rewriting requires a full backup first, a rewrite, and a force-push. Every recorded commit
   hash becomes stale afterwards — cite commits by subject line from then on. Do not begin this
   without explicit approval.

7. **Verify after the sweep.** Run the pattern file again over every surface: each count is zero,
   or each remaining hit is one the policy allows. Then readers who did not perform the sweep
   check the artifact against the same written policy.

8. **Install a check that stops the class returning** — a pre-commit hook or CI step that runs
   the pattern file. Keep the pattern file outside the published tree: a list of forbidden
   strings is itself a leak. Without a check, the sweep is repeated every few months.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Regular expressions only | Paraphrase survives, and the sweep is reported clean |
| Patterns never tested | Zero hits, because the patterns match nothing |
| Surfaces missed | Clean code, and the branch name or PR body is unchanged |
| Metadata stripped in place | A `_original` copy or the PDF's earlier revision still holds it |
| Self-verified | The author reads past their own phrasing |
| History rewritten without backup | Irreversible, and something was lost |
| Pattern file published | The check that guards the class lists every forbidden string |
| No returning check | The class returns within months |

## Report

The written policy, the hit counts per surface before and after, what the independent review
found, whether history was rewritten and what that invalidated, and the check installed to
prevent recurrence.
