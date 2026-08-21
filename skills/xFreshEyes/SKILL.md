---
name: xFreshEyes
description: >-
  Independent audit of an implementation and its written description for methodological flaws
  and internal contradictions, by an agent with no prior context. Report only, change nothing.
  Use when the user asks for fresh eyes, an independent review, a second pass after fixes, or
  asks whether an approach is sound. For "does the code match this document", use xSpecDiff.
user-invocable: true
argument-hint: <subsystem, pipeline or PR to audit>
effort: max
---

# Fresh eyes

An agent that did not build the thing audits whether it is sound, and reports without touching it.

Follow `~/.claude/CONVENTIONS.md`, in particular: verification proves execution, do not rationalize your instrumentation and questions get answers not edits.

## Input

What to audit, and where its written description lives — design doc, paper section, PR body, or
README. Both halves are in scope: an implementation that is internally sound but described
inaccurately is still a finding.

## Procedure

1. **Delegate to a subagent with no prior context.** This is the point of the skill. An agent
   that helped build the thing re-derives the same reasoning and confirms its own choices. Give
   the subagent the target and the description, not your conclusions about them.

2. **Include the bash style rules in the subagent prompt** (bash style), and scope it explicitly:
   read-only, report findings, modify nothing.

3. **Audit for these, in order:**

   | Question | What a finding looks like |
   |---|---|
   | Does the described method match what runs? | The document says one threshold, the code uses another |
   | Is the method sound? | A filter that cannot do what it claims; a metric that cannot separate what it ranks |
   | What is unjustified? | A constant with no measured or published basis (thresholds from measured or published data) |
   | What is unreachable? | Code that never executes, a stage nothing calls (verification proves execution) |
   | What is silent? | A fallback, a default, or a swallowed error (no silent fallbacks) |
   | What contradicts itself? | Two sections, or code and comment, that cannot both be true |
   | What is unrequested? | Behaviour nobody asked for, quietly changing results |

4. **Verify each finding before reporting it.** Give the file and line, and the evidence. A
   suspicion is reported as a question, not as a finding.

5. **Change nothing** (questions get answers not edits). The deliverable is the report. Fixes are a separate decision the
   user makes after reading it.

6. **Run a second pass after fixes land,** with a fresh subagent again. The pass that reviews its
   own corrections is not independent.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Reviewing with the builder's context | Every choice is confirmed; the review finds only typos |
| Auditing code but not its description | The implementation is fine and the paper describes something else |
| Fixing while reviewing | The user loses the chance to decide, and the report no longer matches the tree |
| Unverified findings | Plausible claims that waste a round when they turn out to be wrong |
| Reusing the same agent for the second pass | It defends what it approved before |
| Reporting severity without evidence | "Critical" with no file, line or failing case |

## Report

Findings ranked most severe first, each with file and line, the evidence, and the failure it
causes. Then a short list of what you checked and found sound — this tells the user what the
audit actually covered. State explicitly that nothing was modified.
