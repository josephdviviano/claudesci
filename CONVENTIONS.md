# Conventions

Evidence and process rules for skill work. Skills cite these by name.

**The global `~/.claude/CLAUDE.md` conventions stay in force at all times, including while
following a skill. Nothing here overrides or replaces them.** What `CLAUDE.md` already states —
response style, comment style, commit and PR message style, test style, ASD-STE100 — is not
repeated here. Read it as well as this file.

- **Verification proves execution.** Proving the path ran, not that it compiled. Use `git log -S`,
  call-site grep, startup counters. Relink or rebuild before you believe a log.
- **Do not rationalize your instrumentation.** A number you cannot explain is the finding.
- **Never edit the evidence.** Baselines, recorded data and thresholds are not adjusted to make a
  failure go away.
- **Diagnostics must discriminate.** A measurement must separate the hypotheses agreed with the
  user. "Gather more data" is not a diagnostic.
- **Thresholds from measured or published data.** Never from a format ceiling, and never
  from one sample.
- **No silent fallbacks.** The code must crash if it does not receive the correct inputs, does not
  find the expected data, or hits an internal deadline. These crashes specify that the code is
  broken, which we use to guide development.
- **A changed flow replaces the old one,** unless an additional path is specified explicitly.
- **Commit only when asked.** Commit, push or open a PR on request, never on your own initiative.
  Message style is `CLAUDE.md`.
- **Per-repo policy is authoritative** for formatters, test runner and environment. Read the
  project `CLAUDE.md` and `.pre-commit-config.yaml` first.
- **Questions get answers not edits.** No unrequested optimizations or features.
- **Bash style for autonomy:** no `$()`, no `cd X &&`, no `VAR=` prefixes. Put helper scripts in
  the scratchpad. Repeat this rule inside every subagent prompt.
- **Other sessions share the tree.** A sibling session's uncommitted work looks like yours in
  `git status`. Run `ListAgents` before any git operation that rewrites files (`checkout --`,
  `stash`, `reset`, `bisect`) and before you commit. Message siblings and treat their files as
  read-only until reconciled. Never regenerate a hunk from `HEAD` in a dirty tree: that discards
  every session's work in the hunk. Edit shared files with targeted edits, not whole-file writes:
  a targeted edit fails loudly when a sibling changed the text. Build into a private build
  directory. Hash the artifacts outside the repository that a verification run reads — caches,
  golden files, baked data — and check the hash at each verification, so that before and after
  read the same inputs.
- **Stale docs get deleted,** not archived. They are context pollution.
- **Revise old comments** when the associated code changes.

Compute infrastructure facts that drift (clusters, schedulers, local machine limits) live in
`~/.claude/ENVIRONMENTS.md`, not in skills. Per-repo facts live in the project `CLAUDE.md`.
