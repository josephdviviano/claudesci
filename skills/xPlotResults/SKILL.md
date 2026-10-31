---
name: xPlotResults
description: >-
  Turn the results of completed runs into publication-ready figures and tables by writing a
  reusable script the user can re-run and audit. Use when the user asks for plots, figures or
  result tables from data on disk. Assumes the run set is known-good — use xAnalyzeLogs to
  explain failures first.
user-invocable: true
argument-hint: <results directory> <what the figure must show>
---

# Plot results

The deliverable is the script, not the picture. Anyone must be able to re-run it and check every
number it draws.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: do not rationalize your
instrumentation, never edit the evidence and thresholds from measured or published data.
For chart form, palette and layout, use the `dataviz` skill: this skill does not define appearance.

## Input

Where the results are, and what question the figure must answer. If the run set has not been
reconciled, run `xAnalyzeLogs` first — a mean over a set that silently lost a third of its runs
is worse than no plot.

## Procedure

1. **Write a script, committed to the repository, not an ad-hoc plot.** It takes the data path as
   an argument, needs no editing to re-run, and writes its output to a stated location. A figure
   that cannot be regenerated after this session is not a result.

2. **Load from disk, and never modify the source data.** If the data needs repair, repair
   it in the pipeline that produces it, not in the plotting script.

3. **Declare the axes explicitly:**

   | Axis kind | Treatment |
   |---|---|
   | Nuisance | Aggregated over. State the estimator (mean, median), the interval (for example a 95% bootstrap interval or the standard error) and n in the figure or caption. When n is small, draw each seed as well as the aggregate |
   | Substantive | Distinguished — one line, facet or column each |

   Every configuration field is one or the other, and the script says which. Fields left
   undeclared collapse silently and produce two lines with the same label.

4. **State every filter and exclusion in the output,** not only in the code: how many runs went
   in, how many were dropped, and why.

5. **Equalize the axis that makes the comparison fair** — compute, budget, sample count, wall
   time. A method that ran longer is not a better method.

6. **Print the underlying table beside the figure.** Every drawn value must be traceable to a
   number the user can read, and from there to a file on disk.

7. **Check legibility before returning it:** no two series sharing both label and style, shared
   ranges across facets that are meant to be compared, readable at print size, and axis labels
   with units.

8. **Report anomalies rather than smoothing them.** A discontinuity you cannot explain
   goes in the report, not out of the plot.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Ad-hoc plot | Reproducing the figure means reproducing the session |
| Undeclared nuisance axis | Several configurations collapse into one indistinguishable line |
| Unstated exclusions | Runs dropped for reasons nobody records |
| Unequal comparison | The winning method simply had more compute |
| Figure without its numbers | A value in the paper traces to nothing |
| Band without method or n | The shading could be a standard deviation, a standard error or a min–max range |
| Editing source data to fix a plot | The defect is hidden and the data is now wrong |

## Report

The script path and how to run it, the figures and tables produced, the run counts in and
excluded, which axes were aggregated and which distinguished, the estimator, interval and n of
each aggregate, and any anomaly you could not explain.
