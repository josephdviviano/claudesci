---
name: xAtomicConcepts
description: >-
  Decompose a body of artifacts into the minimal set of atomic units that compose to produce all
  of them, then read redundancy, coverage gaps and novelty off that basis. Use for corpus
  diversity audits, refactoring many implementations to one abstraction, compressing text
  without information loss, and reducing comments to what the code cannot carry.
user-invocable: true
argument-hint: <the body of artifacts to decompose>
effort: high
---

# Atomic concepts

Find the small set of reusable units a large set of artifacts is built from, then use that basis
to say what is redundant, what is missing, and what is genuinely new.

Follow `~/.claude/CONVENTIONS.md`, in particular: do not rationalize your instrumentation and thresholds from measured or published data.

## Input

The artifacts and what the decomposition is for. The purpose decides what counts as an atom:

| Body | Atom | Used for |
|---|---|---|
| Generated problems or tasks | The mechanism a solution must use | Diversity audit, targeted generation |
| Functions or modules | The distinct operation performed | Refactor many implementations to one |
| Paragraphs or sections | The distinct claim made | Compress without information loss |
| Comments | The fact the code cannot state itself | Comment reduction (CLAUDE.md comment style) |
| Configs or scripts | The distinct decision encoded | Deduplicate and harmonize |

## Procedure

1. **State what counts as an atom, before counting anything.** Write the definition down. A
   vocabulary chosen after seeing the results can always be shaped to make a corpus look diverse.

2. **Decompose each artifact into its atom set.** Record the mapping, artifact to atoms, as data
   you can re-derive — not as a summary.

3. **Validate the basis by reconstruction.** Can you rebuild each artifact, at least in outline,
   from its atoms? If not, the atoms are labels rather than a basis, and every count below is
   meaningless.

4. **Read the structure off the mapping:**

   | Measure | Question it answers |
   |---|---|
   | Atom frequency | Which atoms are ubiquitous, which are rare |
   | Identical atom sets | Which artifacts are the same thing in different surface form |
   | Absent atoms | What the body never exercises |
   | Composition depth | Whether "harder" artifacts are just more atoms, or different ones |

5. **Distinguish surface from substance.** Different geometry, different names, different wording
   are not different concepts. Two artifacts with the same atom set are duplicates however
   different they look.

6. **Check any derived metric against outcomes before trusting it** (do not rationalize your instrumentation). A difficulty or
   novelty score computed from the basis must be shown to predict something real. Report it as
   unvalidated until it does.

7. **Act on the basis** according to the purpose: delete redundant artifacts, generate for absent
   atoms, extract the shared abstraction behind duplicate implementations, or cut text that
   repeats a claim already made.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Vocabulary defined after the fact | The corpus is exactly as diverse as the definition was built to show |
| Counting without reconstruction | The atoms do not compose back, and the analysis measures nothing |
| Surface counted as substance | N variations of one artifact reported as N distinct artifacts |
| Novelty measured on the wrong axis | Rare surface features ranked as new concepts |
| Trusting an unvalidated score | A ranking that turns out to predict nothing is used to curate |
| Deleting before validating | Redundancy removed on a basis that was wrong |

## Report

The atom definition, the basis with frequencies, the redundancy groups, the absent atoms, and
what you propose to do with each. Mark every derived score as validated or unvalidated, and say
against what.
