---
name: xTriageReport
description: >-
  Carry a numbered list of observations from a real run to closure, item by item. Use when the
  user returns from a playtest, a pipeline execution or a manual inspection with several
  findings at once, or reports that an earlier item is still not fixed.
user-invocable: true
argument-hint: <the observation list, or the item numbers to revisit>
---

# Triage report

Track every reported observation independently until the user confirms it on a re-run.

Follow `~/.claude/CONVENTIONS.md`, in particular: diagnostics must discriminate, commit only when asked and questions get answers not edits.

## Input

The user's list, in their words and their numbering. Identifiers they include — object, level,
mission, run id, coordinates, timestamps — are part of the item, not decoration.

## Procedure

1. **Build the item table from their list.** Keep their numbering permanently: they will refer to
   "item 3" in the next message and for weeks afterwards. Never renumber, never reorder, never
   silently drop an item you could not reproduce.

2. **Restate each item as an observation** with its identifiers, separated from any cause the
   user proposed. Their hypothesis is a candidate, recorded as such (see `xHypothesisDebug`).

3. **Ask for what you need to reproduce,** per item. Do not guess at a missing identifier.

4. **Give every item a status** and keep it current:

   | Status | Meaning |
   |---|---|
   | open | Not yet reproduced |
   | reproduced | Seen locally, cause unknown |
   | diagnosed | Cause proven, not yet fixed |
   | awaiting confirmation | Fixed locally, user has not re-run |
   | confirmed | User confirmed on a re-run |
   | regressed | Was confirmed, has returned |

5. **Diagnose each item on its own.** Do not merge two items into one fix unless you have proven
   one cause explains both — and say so explicitly when you do.

6. **Never move an item to confirmed on a passing test.** Tests show the case you wrote. The user
   reported what they saw. Only their re-run closes the item.

7. **Report the whole table every round,** not only what changed. The user is tracking items you
   have said nothing about, and a silent item reads as a dropped one.

8. **Do not add items they did not raise** (questions get answers not edits). If you find something adjacent, list it
   separately as a new finding for them to accept or decline.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Collapsing items | Three observations answered by one fix; two of them still occur |
| Closing on a green test | "Fixed" reported, and the user's next run shows it unchanged |
| Renumbering | The user says "item 3" and means something else than you do |
| Silent drops | An item you could not reproduce vanishes from the table |
| Symptom clearing | The visible artifact stops and the mechanism is untouched |
| Scope creep | Unrequested changes arrive with the fixes, and confound the re-test |

## Report

The full item table with statuses, then one line per item changed this round: what the cause
was, what changed, and what the user should look at on their re-run. List items awaiting
confirmation last, since that is the list they will act on.
