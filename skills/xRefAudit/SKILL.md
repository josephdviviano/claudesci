---
name: xRefAudit
description: >-
  Audit a manuscript's references on two axes: whether each entry's metadata is correct against
  the registration record, and whether each cited work actually supports the claim made at its
  citation site. Produces a hand-verifiable worksheet, changes nothing, then answers fix-up
  questions while the user edits. Use whenever the user asks to check references, citations or a
  bibliography, asks whether a citation is correct or defensible, worries about hallucinated
  references, asks "did I cite this right", or is preparing a paper for submission. For
  justifying a new threshold from published practice before it enters the paper, use xLitGround.
user-invocable: true
argument-hint: <manuscript to audit, or an item number to discuss>
effort: max
---

# Reference audit

Two questions per citation: does the reference exist as described, and does it support the
sentence it is attached to. The second finds almost all the real errors and is the one people
skip.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: never edit the evidence, questions
get answers not edits and bash style for autonomy.

## Input

The manuscript and its bibliography. Paths, not a description. If the project splits prose
across files or has a deprecated tree, find them all: a stale copy can carry a live citation to
a key that no longer exists.

## The two axes

| Axis | Question | Typical finding |
|---|---|---|
| Metadata | Does this entry match the registration record? | Wrong venue, missing authors, stale preprint version, superseded author name |
| Defensibility | Does the cited work support this exact claim? | A number the source does not contain; a claim the source contradicts |

Both matter, and they fail independently. An entry can be field-perfect and attached to a
sentence its paper argues against.

## Procedure

### Phase 1: structural pre-pass, before any network call

Cheap, fast, and it finds a class of defect no amount of web verification will. Script it.

1. **Cross-check keys both ways.** Keys cited but not defined break the build. Keys defined but
   never cited are clutter, and sometimes evidence of a citation that got detached from the thing
   it was meant to support.
2. **Separate active citations from commented-out ones.** A key cited only inside `%` comments is
   effectively uncited, and an undefined key hiding in a comment is a trap that fires the moment
   someone uncomments the block. Report both states; do not conflate them.
3. **Build a per-key usage map**: for every key, every line number and the surrounding sentence.
   This is the input to Phase 3, and it is also how you notice one entry carrying four unrelated
   claims.
4. **Find tools, datasets and software named in prose with no citation attached.** Check the
   unused-entry list against these names: an unused entry plus an uncited tool name is usually
   one detached citation, not two problems.
5. **Check for duplicate entries, brace balance, and missing required fields.**

### Phase 2: metadata, from raw registration records

Split the entries into batches of twelve to fifteen and delegate one subagent per batch. Include
the bash style rules in every subagent prompt.

**Read raw records, never a summarizing fetch of a publisher page.** This is not fastidiousness.
A summarizing fetch of one bioRxiv page silently dropped three real authors, and returned three
mutually contradictory author lists for the same URL across three attempts. Registration records
are machine-readable and authoritative; a page summary is neither.

| Want | Use |
|---|---|
| Journal or conference DOI | `https://api.crossref.org/works/<doi>` |
| arXiv DOI | DataCite, `https://api.datacite.org/dois/<doi>`. Crossref has no deposit for these |
| arXiv metadata | `http://export.arxiv.org/api/query?id_list=<id>` |
| PubMed record | NCBI E-utilities, or Europe PMC `resultType=core` |
| Open-access full text | Europe PMC `/<PMCID>/fullTextXML` |
| Conference acceptance | The official proceedings page, and the camera-ready footer |

Verify every field, and resolve every DOI to confirm it lands on that paper and not a different
one. Then three things that are easy to miss:

- **Live metadata can disagree with the frozen PDF, and the live record usually wins.** An author
  who changes their name updates the indexes; the camera-ready PDF and the proceedings DOI keep
  the old one forever. When records disagree, report the disagreement and its direction rather
  than picking silently. Whether to follow a name change is the author's call, not yours.
- **Preprints drift between versions.** The DOI serves the current version, so an author list
  captured from v1 leaves a reader seeing a different list from the one you printed. Check the
  version the DOI actually resolves to.
- **A preprint is not a published paper, and a workshop is not a main conference.** Check both
  directions: a preprint entry whose work has since appeared, and an entry claiming a venue the
  work never had.

### Phase 3: defensibility, claim by claim

Delegate by manuscript section, with the usage map. For each site, decide whether the source
supports the claim **as worded**:

| Verdict | Meaning |
|---|---|
| Supported | The source states this |
| Partially supported | Topically right, but not this specific quantitative or causal claim |
| Not supported | The source does not contain this |
| **Contradicted** | The source argues the other way |
| Unverifiable | Say what you tried, and why it failed |

Contradicted is its own verdict because it is the most serious and the easiest to miss. The worst
finding in the audit this skill came from was a footnote whose first half quoted a real figure and
whose second half asserted something the cited paper spends two paragraphs arguing against.

Four patterns that account for most real findings:

1. **Every number attributed to a source must be found in that source.** Search the full text for
   the figure. Numbers get carried between drafts and detach from their origin.
2. **A grouped `\citep{a,b}` hides per-key errors.** A description can be exactly right for one
   key and wrong on both counts for the other. Assess each key separately, then recommend
   splitting rather than rewriting.
3. **Understating is still misattribution.** If the source found an effect stronger than the
   manuscript claims, that is an error too, and a reviewer who checks will notice.
4. **Check the noun, not just the adjective.** A claim can name the wrong axis entirely: a
   generalization failure attributed to one variable when the source measured another and found
   it held.

### Phase 4: independent cross-check

Delegate the assembled finding list to one fresh agent that has not seen your reasoning, and ask
it to confirm or refute each item from primary sources. Tell it plainly that **a false finding
reported to the author is worse than a missed one**, because the author will spend real time
disproving it and will trust the rest of the list less.

Expect it to downgrade some items. That is the point, and those downgrades are the most valuable
output of the phase. Verify anything extraordinary yourself, with your own tool calls, before it
reaches the user.

### Phase 5: the worksheet

The deliverable is a markdown file the user works through by hand, not a message. Every item
carries six things, and the fourth is what makes it verifiable rather than merely assertable:

```
## [T1-01] `file:line` : one-line title
- [ ] Verified

**Cited:** the bibtex key and what it is

**Current text:**
> the exact text, quoted

**What I found:** what the source says, quoted, with the gap named

**Verify at:** a URL, preferring an open-access mirror
**Search for:** the exact string to find on that page

**Action:** what to change, or what decision is needed

**Confidence: high/medium.** And why. Say plainly when a source was paywalled and the
verdict rests on the abstract.
```

Tier the items by the kind of action they need, so the user can stop where the value runs out:
claims the source does not support, then decisions only the author can make, then metadata
fields, then precision and mechanical, then optional non-errors.

**Close with what you checked and found correct.** Name the entries and the claims. This is not
padding: without it the author re-verifies work you already did, and it tells them what the audit
actually covered. Warn them off any false correction you can foresee, such as a page range that
looks wrong but matches the registration record, or an unfamiliar DOI prefix that is real.

### Phase 6: question-and-answer mode, while they edit

The audit is the start of the work, not the end. Stay in this mode until the user leaves it.

- **Answer, do not edit.** They are editing the manuscript; you
  are the reference desk. Supply proposed replacement text on request, as a block they paste.
- **Re-verify before endorsing.** When they ask about an item, read the source again rather than
  quoting your own earlier finding. Revising your own verdict is a good outcome, and saying so
  explicitly is better than quietly carrying an error forward.
- **When they propose a fix, check that it actually fixes it.** A reworded adjective around the
  wrong noun is still wrong. Say which part the change repairs and which part it leaves.
- **Keep the item numbering.** They will say "T1-06" for days.
- **Minimal text on request means minimal.** Count the words you are adding and say the count.
- **On "is this novel", search for prior art and never certify absence.** Separate the layers: a
  standard technique, an instantiation of a published framework, and the one specific step that
  might be new. Report near neighbours with their venue verified, and say what you could not rule
  out. Finding prior art that repairs a weak justification is a better outcome for the author than
  a novelty claim they would have to defend.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Auditing the bibliography only | Every field is perfect and half the claims are unsupported |
| Trusting a page summary for an author list | Names silently dropped; two runs disagree |
| Treating the PDF as authoritative on metadata | A name change or a published version is missed |
| Editing the manuscript | The author loses the decision, and the worksheet no longer matches the file |
| Reporting a finding without a verify-at string | The author cannot check it, so they either trust it or redo it |
| Uniform confidence | An abstract-only verdict is presented like a full-text one |
| Omitting what was correct | The author re-verifies seventy entries for nothing |
| Skipping the cross-check | A wrong finding wastes the author's time and discredits the list |
| Renumbering between rounds | "T1-06" means two different things |

## Report

The worksheet path, then in the message: the reassuring global result if there is one, the
tier-one items with enough detail to act on, the decisions you need from the author as explicit
questions, and a count of what sits in the lower tiers. State that nothing was changed.
