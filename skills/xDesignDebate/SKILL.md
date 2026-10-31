---
name: xDesignDebate
description: >-
  Interrogate a proposed mechanism to sign-off without writing any code. Use when the user wants
  to discuss, debate or defend a design, is suspicious a proposal is overcomplicated, or is
  thinking out loud rather than requesting a change.
user-invocable: true
argument-hint: <the design or mechanism to debate>
effort: xhigh
---

# Design debate

Argue the design to a conclusion. Write nothing until the user signs off.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: questions get answers not edits,
thresholds from measured or published data and no silent fallbacks.

## Input

The proposal, whoever made it. The user's own proposals are argued with equally — they ask for
push-back and expect it.

## Procedure

1. **Write no code.** Not an experiment, not a prototype, not a small test to check an intuition.
   Implementing during a design discussion removes the user's decision and is the failure this
   skill exists to prevent.

2. **State the proposal back in its simplest form,** with what it costs and what it assumes. If it
   cannot be stated simply, that is the first finding.

3. **Ask what problem it solves, and what would happen without it.** A mechanism that survives its
   own removal is not needed.

4. **Attack the proposal on these axes:**

   | Axis | Question |
   |---|---|
   | Necessity | What breaks if this is removed entirely? |
   | Simplicity | Are two mechanisms doing one job? Can they be one? |
   | Justification | Where does each constant and choice come from? |
   | Failure behaviour | What does it do when its assumptions do not hold? |
   | Coupling | Does it force two things to be tuned together that could be independent? |
   | Explainability | Can it be explained to a collaborator in one paragraph? |

5. **Defend your own proposals when challenged, or concede plainly.** State the reason a choice is
   right, or say it is not and why. Do not restate the proposal in new words as a defence.

6. **Offer the simpler alternative** whenever one exists, including doing nothing.

7. **Record the conclusion and the reasons it was reached,** so the decision is not re-litigated
   in a later session. Discarded options are recorded with why they were discarded.

8. **Stop at sign-off.** Implementation is a separate turn, on the user's word.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Building during the debate | Files change while the design is still open |
| Agreeing to close the discussion | The weak proposal survives because nobody argued |
| Defending by restatement | The same claim in new words, presented as an answer |
| Complexity accepted as sophistication | Two mechanisms kept because each sounds reasonable |
| Conclusion not recorded | The same debate happens again next month |
| Answering a question with an edit | The user asked what something does and the code changed |

## Report

The proposal, the axes it survived, the axes it failed, the alternatives considered and why they
were discarded, and the conclusion — stated as a decision the user can approve or reject.
