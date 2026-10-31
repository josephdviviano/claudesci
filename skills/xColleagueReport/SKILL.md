---
name: xColleagueReport
description: >-
  Produce a shareable report of a result or system for collaborators, with the methods written
  out and the numbers reproducible. Use when the user wants something to send to colleagues, to
  show in a meeting, or to convince a collaborator that a contribution is substantive.
user-invocable: true
argument-hint: <what the report must cover, and who reads it>
effort: xhigh
---

# Colleague report

Write for a reader who will check your work, not take your word for it.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: do not rationalize your
instrumentation and commit only when asked.

## Input

The result or system to describe, and the audience. A domain expert reviewing a method and a
collaborator deciding whether to adopt it need different documents.

## Procedure

1. **Ask what decision the report supports.** Adopt this method, trust this number, or approve
   this design. The decision determines what must be in it and what is noise.

2. **Write the methods out in full.** State the losses, the equations, the filter criteria, the
   thresholds. Naming a method and citing it is not enough for a reader who must check whether it
   is the right one. Where the user is not the domain expert, spell out conventions explicitly so
   the expert can verify them.

3. **Make every number reproducible.** Give the script, the data location, and the run set behind
   each figure and table. Produce figures with `xPlotResults` so the script exists.

4. **Include negative and null results.** "The two losses are equivalent" is a result, and
   suppressing it wastes a colleague's month.

5. **State what is not established** — assumptions, untested claims, the parts that rest on one
   run. A report that distinguishes proven from assumed is trusted; one that does not is checked
   line by line.

6. **Make it runnable where that helps.** Commit the report and its scripts so colleagues can run
   them locally. A draft PR is a good sharing mechanism and keeps the work isolated from
   submitted results.

7. **Choose the medium for how it will be read:** markdown in the repository for people who will
   run it, a rendered page for a meeting, a PDF for people outside the repository.

8. **Check what leaves the repository.** Unpublished results, identifying information or
   restricted material need `xSanitize` before the report is shared.

9. **Do not commit, push or open the PR unless asked.**

## Common mistakes

| Mistake | How it appears |
|---|---|
| Method named, not written | The reader cannot tell which variant was run |
| Numbers without provenance | A table nobody can regenerate or check |
| Negative results omitted | The colleague repeats the experiment you already ran |
| Proven and assumed mixed | Every claim gets re-derived because none is marked |
| Report that cannot be run | Questions come back as requests for the script |
| Overclaiming | One seed described as an effect |

## Report

Where the report lives, what it claims, what it explicitly does not establish, and how a reader
regenerates each number.
