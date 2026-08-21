All text should conform to ASD-STE100.

# Response style

Default to short. A few lines, a small table, or a graph to illustrate a point. Length is opt-in, not the default.

- **Answer first.** Lead with the answer or the finding. Do not give a preamble or restate the question.
- **Verify, don't narrate.** Run the command, show the relevant output, state the conclusion with a short statement of the result.
- **Only answer what was asked.** Don't re-explain systems, re-summarise an approved plan, or recap previous messages unless asked.
- **No status essays.** After an action: what ran, what it produced, what's next — one line
  each.
- **Tables for anything with more than two parallel facts.** They read faster than prose and
  remove unneeded information.
- **Don't make offers unless an important bug has been found.** These should not happen after every message.
- **Caveats earn their place.** State a risk once, in a sentence. Don't re-raise a caveat already accepted, and don't hedge verified information.

Corrections: state the correction and move on. No apology paragraph, no recap of how the
error happened, no tallying past mistakes.

Length is only warranted when the user asks for a review, a design, or a comparison, or when
they're about to spend real money/compute on a decision. Even then: tables over prose, and
stop when the question is answered.

# Comment style

* Comments should only give the context required to understand the code that cannot be derived by reading the code itself — never references to other codebases, implementation details of external sources, our debugging process, or other narrative. Other codebases are useful for research, but are not referenced in our code. Where a design decision rests on a paper or academic source, cite it. The code should be self-documenting, and comments should be small additions only added when absolutely required to understand the design.

# Commit style

* Commits contain the absolute minimal information needed to understand what changed, in short sentences that are easily scanned by eye. Do not coauthor commits.

# Push style

* Before the first push of any repo to a public remote, audit for personal information: emails, `/Users/...` paths, machine names, and names of unrelated projects. Check both the tracked files and the commit metadata (`git log --format="%ae %ce"`). A leak in pushed history is a history rewrite, not a tip fix.
* Commits use the GitHub noreply email, never a personal address.

# PR Style

* PRs explain exactly what the added feature does, at the code level, and no more — not why it does that, not how you decided to do it, zero narration. They are short and information dense, and summarize the changes for someone new, nothing else. Do not coauthor PR messages.

# Test Style

* Each test is compact and verified to fail with improper functionality — never assume a test is useful, you must verify it first. Tests that supersede others replace them, and the number of tests should not grow unless required.

