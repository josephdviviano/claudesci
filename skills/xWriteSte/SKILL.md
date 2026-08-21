---
name: xWriteSte
description: >-
  Compress a document section into ASD-STE100 Simplified Technical English without losing
  information, to a page or word budget, then re-verify it against the code it describes. Use
  when the user asks to condense, simplify or shorten text, or to fit a page limit.
user-invocable: true
argument-hint: <section to compress> [budget]
---

# Write STE

Make the text shorter and clearer without dropping a fact.

Follow `~/.claude/CONVENTIONS.md`, in particular: questions get answers not edits and stale docs get deleted.

## Input

The exact section, and the budget. Edit only what was named — a compression pass that spreads
into neighbouring sections is unreviewable.

## Procedure

1. **Inventory the facts in the section first.** Every claim, number, threshold, condition and
   qualifier, listed before you rewrite. This list is what you check the result against.

2. **Rewrite to Simplified Technical English:** short active sentences, one idea each, consistent
   terms for the same thing, no synonym variation for elegance. Remove hedges, throat-clearing
   and transitions that carry no fact.

3. **Compress by removing repetition, not information.** The same claim made three ways becomes
   one. `xAtomicConcepts` finds these groups when the text is long.

4. **Check the result against the inventory.** Every fact still present, unchanged in meaning.
   Numbers and conditions are where loss happens: a qualifier dropped changes the claim.

5. **Verify the compressed text against the code it describes.** Compression is a common moment
   for text to drift from the implementation. Use `xSpecDiff` for a long or high-stakes section.

6. **Keep to the budget,** and report what it cost. If the budget cannot be met without dropping
   a fact, say which fact and let the user decide (questions get answers not edits).

7. **Do not add.** No new framing, no smoothed-over gaps, no invented justification for a number.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Qualifier dropped | "Under these conditions" removed, and the claim becomes false |
| Terms varied | The same object called three names; the reader thinks there are three |
| Compressed into inaccuracy | Two steps merged into one sentence that describes neither |
| Spread beyond the section | Untouched sections are edited and the diff is unreviewable |
| Text no longer matches code | The description was compressed toward what it should say |
| Silent fact loss | Shorter text, no record of what was cut |

## Report

The section, the before and after size against the budget, and the fact inventory with each item
confirmed present. List anything cut and why, and any drift from the code you found while
checking.
