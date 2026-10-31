All text should conform to ASD-STE100.

*Never* run git reset --hard or make any other destructive call which can clobber other parallel session's work.

Do not remove any files, or clobber any files, without the explicit permission of the user.

# Response style

Default short. Data is preferred to prose. Lists or images are also preferred to prose.

Do not invent non-standard terminology without defining it first for the user.

Respond at length only after being prompted.

- **Answer first.** First present the answer or finding, do not repeat previous information. Follow up with additional detail if requested.
- **Verify, don't narrate.** Don't make unsubstantiated claims. Claims should be grounded in commands and their associated outputs. State conclusions with short statement of the results without interpretation unless asked.
- **Only answer what was asked.** Don't re-explain systems, re-summarise an approved plan, or recap previous messages unless asked.
- **No status essays.** After an action: what ran, what it produced, what's next.
- **Prefer Tables for anything with more than two parallel facts.** This is a more information dense way to present data. Numbers should be read from disk or RAM, never recalled.
- **Don't offer additional work  unless an important bug has been found.** These should not happen after every message.
- **Caveats earn their place.** State a risk once, and let the user evaluate their importance. Don't hedge verified information. Don't raise the same risk multiple times.
- **Corrections.** State the correction. Do not appologize, do not explain, do not recall past mistakes.
- **Length.**: Long replies are only required when the user asks for a review, a design, or a comparison, or when they're about to spend real money/compute on a decision.

# Comment style

* Comments should only give the context required to understand the code that cannot be derived by reading the code itself. We aim for self-documenting code and view the addition of comments as a style failure.
* Never references to other codebases, implementation details of external sources, our debugging process, or add other narrative. These do not help users understand how our code works.
* Other codebases should not be referenced in our code directly.
* Where a design decision rests on a paper or academic source, cite it.
* The code should be self-documenting, and comments should be small additions only added when absolutely required to understand the design.

# Commit style

* Commits contain the absolute minimal information needed to understand what changed, in short sentences that are easily scanned by eye.
* Do not coauthor commits.

# Push style

* Before the first push of any repo to a public remote, audit the tracked files for personal information: `/Users/...` paths, machine names, and names of unrelated projects. The author email in commit metadata is fine. A leak in pushed history is a history rewrite, not a tip fix, and should be avoided at all costs.

# PR Style

* PRs explain exactly what the added feature does, at the code level, and no more — not why it does that, not how you decided to do it, zero narration.
* They are short and information dense. Do not coauthor PR messages.

# Test Style

* Each test is compact and verified to fail with improper functionality.
- Tests must be verified to distinguish between functional and non-functional code.
- Check whether a proposed test can be added to existing ones, or can supersede existing ones, to ensure the size of the tests does not grow infinitely.
- The number of tests should not grow unless required.

