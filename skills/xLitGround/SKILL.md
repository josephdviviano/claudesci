---
name: xLitGround
description: >-
  Justify a threshold, setting or design choice from published practice rather than a local
  pilot, and verify every citation before it enters a paper or the code. Use when a constant
  needs defending, when the user asks what others use, or when a claim is about to be cited.
user-invocable: true
argument-hint: <the choice or claim to ground>
---

# Lit ground

Give a number a defensible source, and check that the source says what you claim it says.

Follow `~/.claude/CONVENTIONS.md`, in particular: thresholds from measured or published data.

## Input

The choice to justify, and where the justification will end up — a config default, a paper
sentence, or a design decision. Include any claim the user made: their claims get verified too,
and they will ask you to.

## Procedure

1. **State what would count as grounding** before searching. A widely used default, a value
   reported in comparable settings, or a standard from the field. Decide this first, or you will
   accept whatever you find.

2. **Search published practice,** preferring what is widely used over a single paper, and
   documented tool defaults over folklore.

3. **Read the source, not the abstract.** Confirm the value, and confirm the context it was
   measured in.

4. **Record the regime with the value.** A threshold measured on different data, at a different
   scale, or for a different objective is not grounding for your case. If you transplant it, say
   so and say why it should carry over.

5. **Verify the user's claims before citing them.** They will often be right and will still ask
   you to check. Report the check either way.

6. **Check provenance where it matters.** For a pretrained model or a benchmark, what was it
   trained on? An overlap with your evaluation set is a criticism a reviewer will raise.

7. **If nothing published applies, say so plainly,** then measure the distribution yourself and
   label it as local evidence (thresholds from measured or published data). Do not dress a pilot measurement as an established value.

8. **Record the decision and its citation** where it will not be re-litigated — the design doc or
   the config comment, not the conversation.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Citing from memory | The paper exists, and does not contain the number |
| Abstract-only reading | The value is real and applies to a different setting |
| Regime transplant | A threshold from another scale or dataset is used unmodified |
| Pilot dressed as practice | "Standard" describes one local run |
| Unverified claim propagated | The user's aside enters the paper as a citation |
| Ignoring training-data overlap | The result is questioned as leakage after submission |

## Report

The choice, the value adopted, the source with its exact location, the regime it came from, and
whether it transfers. Report failed checks explicitly — a claim you could not verify matters
more than the ones you could.
