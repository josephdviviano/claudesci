---
name: xMetricValidation
description: >-
  Validate a new reward, oracle, score or metric before it is trusted: direction, range, failure
  paths, correlation with existing metrics, and whether it predicts what it claims to. Use when
  a new scoring function is wired in, or when a metric's behaviour is questioned.
user-invocable: true
argument-hint: <metric or reward to validate>
---

# Metric validation

Establish what a new metric actually measures before anything optimizes against it.

Follow `~/.claude/CONVENTIONS.md`, in particular: do not rationalize your instrumentation, thresholds from measured or published data and no silent fallbacks.

## Input

The metric, what it is meant to reward, and the metrics already in use alongside it.

## Procedure

1. **Confirm the direction on known cases.** Construct inputs you know are better and worse, and
   check the metric orders them that way. A sign error here inverts training and is invisible in
   the loss curve.

2. **Establish the range and scale.** Bounded or unbounded, typical spread on real data, and how
   it compares in magnitude to the other terms it will be combined with. A term two orders of
   magnitude larger than its neighbours silently dominates.

3. **Test the failure paths.** Empty input, degenerate input, missing values, out-of-domain
   input. The metric must fail loudly rather than return a plausible number (no silent fallbacks). Confirm it
   cannot produce NaN or infinity during training, and check what happens downstream if it does.

4. **Correlate against existing metrics.** Report the correlation and interpret it:

   | Observation | What it means |
   |---|---|
   | Near-duplicate of an existing metric | It adds cost, not information |
   | Correlated where you expected opposition | One of the two does not measure what its name says |
   | Uncorrelated with everything | Either genuinely new, or measuring noise |

5. **Check calibration if it claims a probability or a confidence,** not only ranking accuracy.
   Ranking well and being calibrated are different properties, and they are often confused.

6. **Test whether it predicts the outcome it is used for.** A difficulty score must correlate with
   observed difficulty; a quality score with observed quality. Report the rank correlation. Until
   this is done the metric is unvalidated, and must be labelled that way wherever it is used.

7. **Explain anomalies rather than accepting them** (do not rationalize your instrumentation). If two metrics correlate in a
   direction that contradicts their definitions, that is a finding about one of them.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Direction unchecked | Training optimizes away from the goal and the loss looks healthy |
| Scale unchecked | One term dominates a weighted sum and the others are decorative |
| Silent NaN handling | A missing value becomes a plausible score |
| Correlation not interpreted | A duplicate metric is added and reported as a new signal |
| Ranking taken as calibration | A confidence value that ranks well and is systematically wrong |
| Never tested against outcomes | A score used for curation that predicts nothing |

## Report

Direction, range, failure-path behaviour, the correlation table with interpretation, calibration
if claimed, and the outcome-prediction result. State plainly whether the metric is validated,
and for what use.
