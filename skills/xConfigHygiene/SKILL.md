---
name: xConfigHygiene
description: >-
  Remove silent defaults and fallbacks, move tunables into configuration, harmonize launch
  scripts, and keep past experiments reproducible. Use when a value may be set implicitly, when
  launch scripts have diverged, or when an old experiment can no longer be reproduced.
user-invocable: true
argument-hint: <config, scripts or pipeline to audit>
---

# Config hygiene

Every value that affects a result is set explicitly, in one place, and recorded.

Follow `~/.claude/CONVENTIONS.md`, in particular: thresholds from measured or published data, no silent fallbacks and per-repo policy is authoritative.

## Input

The configuration system, launch scripts or pipeline to audit.

## Procedure

1. **Trace every result-affecting value to where it is set.** Seeds, learning rates, thresholds,
   data paths and splits, reward weights, decay terms. For each, identify whether it comes from
   configuration, a script argument, an environment variable, or a hard-coded default.

2. **Eliminate silent defaults on result-affecting values** (no silent fallbacks). A value that falls back
   without announcing itself produces results nobody can attribute. Prefer failing when it is
   absent over supplying a default.

3. **Find shadowing.** A hard-coded value that overrides configuration, or a default applied after
   the config is read, makes the configuration a decoration. Check the order in which values are
   resolved.

4. **Find inert keys** — configuration nothing reads, or reads and ignores. These are worse than
   absent: they suggest control that does not exist. Remove them (`xDeslop`).

5. **Move tunables into configuration** where the user tunes them by hand, keeping parallel
   configuration files at key parity so one does not silently lack a knob the other has.

6. **Harmonize launch scripts to one convention.** Where scripts differ, establish which
   differences are deliberate before removing any. Explain the deliberate ones to the user rather
   than flattening them.

7. **Check that past experiments can still be reproduced.** If the configuration schema moved,
   provide the path by which an earlier run's settings can still be expressed, or state plainly
   that it cannot and what was lost.

8. **Verify each value is actually read** (verification proves execution). Wiring a key into a file proves nothing until
   something consumes it.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Silent default on a seed | Runs are not reproducible and nothing indicates why |
| Hard-coded value shadowing config | Changing the config has no effect and the user debugs the wrong file |
| Inert keys | A knob that appears to control something and does not |
| Config parity broken | One environment's file lacks a key, and behaviour differs by environment |
| Scripts flattened | A deliberate difference between clusters is removed and jobs fail |
| Key added, never read | The audit reports success and nothing changed |

## Report

The value-to-source table, the silent defaults and shadowing found and what was done, inert keys
removed, script differences kept and why, and whether past experiments remain reproducible.
