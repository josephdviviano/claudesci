---
name: xDebugHarness
description: >-
  Automate a manual debugging loop so it runs headless, repeatably and unattended. Use when the
  user is repeating steps by hand to observe a defect, says they are tired of doing it manually,
  or asks for a harness, an automated fly-through, or systematic instrumentation.
user-invocable: true
argument-hint: <the manual loop to automate>
---

# Debug harness

Turn a hand-driven observation loop into a command that runs start to finish without a human.

Follow `~/.claude/CONVENTIONS.md`, in particular: verification proves execution, no silent fallbacks and bash style.

## Input

The loop as the user performs it, including how they set up, what they look at, and how they
stop. Ask for the parts you did not see rather than inventing them.

## Procedure

1. **Write the manual loop down step by step,** including setup and teardown. Anything you cannot
   describe, you cannot automate.

2. **Automate the whole loop, entry and exit included.** Start the process, drive it to the state
   of interest, capture, and terminate on its own. A harness that needs a human to close a window
   or kill a process has not removed the manual work.

3. **Drive to the state programmatically.** Move the camera, step to the tick, seek the epoch,
   inject the input. Do not wait for a human to arrive at the state.

4. **Exercise the real path.** The harness must run the same code path as the real case,
   including its transport and its side effects. A simplified stand-in reproduces its own
   behaviour, not the defect's.

5. **Sweep the range, do not sample a point.** One parameter value tells you about that value.
   Sweep the interval the defect is suspected to live in.

6. **Emit per-item records before aggregates.** Print the individual rows, then any summary. An
   aggregate hides the single item that disagrees, which is usually the finding.

7. **Make fallbacks loud** (no silent fallbacks). Any path the harness takes when it cannot do the real thing
   must announce itself in a greppable form, or you will read its output as a real measurement.

8. **Confirm the artifact under test is current** before you believe any output (verification proves execution). Rebuild
   or relink first; a harness reading a stale binary produces confident, wrong numbers.

9. **Return the exact command,** with absolute paths and no placeholders, so the user can run it
   themselves.

10. **Keep helper scripts in the scratchpad** unless the project wants them tracked. Do not
    commit without being asked (commit only when asked).

## Common mistakes

| Mistake | How it appears |
|---|---|
| Manual teardown | The run completes but the process stays open; the loop still needs a person |
| Simplified stand-in | The harness passes while the real case fails |
| One sample | A single parameter value stands in for the range |
| Aggregates only | The mean looks fine and the outlier that matters is invisible |
| Silent fallback | A default path is taken and its output is read as measurement |
| Stale artifact | The binary predates the change under test |
| Untrustworthy timings | Measured on a loaded machine or on battery, then compared against earlier numbers |

## Report

State what the harness automates, the command to run it, the range it sweeps, and what its
output is trusted to show. Name anything still done by hand.
