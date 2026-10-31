---
name: xMetricValidation
description: >-
  Validate a new reward, oracle, score or metric before it is trusted: direction, range, failure
  paths, correlation with existing metrics, whether it predicts what it claims to, what an
  optimizer can exploit in it, and, for an LLM judge, agreement with humans and its biases. Use
  when a new scoring function is wired in, when an LLM is used as a judge, or when a metric's
  behaviour is questioned.
user-invocable: true
argument-hint: <metric or reward to validate>
effort: xhigh
---

# Metric validation

Establish what a new metric actually measures before anything optimizes against it.

Follow `${CLAUDE_SKILL_DIR}/../../CONVENTIONS.md`, in particular: do not rationalize your
instrumentation, thresholds from measured or published data and no silent fallbacks.

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
   input. The metric must fail loudly rather than return a plausible number. Confirm it
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

7. **Read what the metric rewards most.** Read the highest-scoring outputs, not only the
   averages. Then optimize against the metric briefly — a short training run, or a search over
   candidates — and read the new top outputs. An optimizer finds the cheapest way to score:
   length, repetition, a formatting quirk, an edge case of the scorer. If the top outputs are not
   what the metric claims to reward, the metric is not ready to optimize against.

8. **Validate an LLM judge as a measuring instrument.** Measure agreement with human labels on a
   held-out set, and report it with a chance-corrected statistic such as Cohen's kappa. Swap the
   order of compared items to test position bias. Compare scores against length at fixed quality
   to test length bias. Test self-preference when the judge's model family also produced
   candidates. Record the judge's model, version and prompt: a change to any of them is a change
   to the metric.

9. **Explain anomalies rather than accepting them.** If two metrics correlate in a direction that
   contradicts their definitions, that is a finding about one of them.

## Common mistakes

| Mistake | How it appears |
|---|---|
| Direction unchecked | Training optimizes away from the goal and the loss looks healthy |
| Scale unchecked | One term dominates a weighted sum and the others are decorative |
| Silent NaN handling | A missing value becomes a plausible score |
| Correlation not interpreted | A duplicate metric is added and reported as a new signal |
| Ranking taken as calibration | A confidence value that ranks well and is systematically wrong |
| Never tested against outcomes | A score used for curation that predicts nothing |
| Top outputs never read | The policy learns the scorer's blind spot, and the score rises |
| Judge unvalidated | The judge prefers the longer answer or the first one, and the ranking follows |
| Judge changed silently | A model or prompt update moves every score, and the shift is read as progress |

## Report

Direction, range, failure-path behaviour, the correlation table with interpretation, calibration
if claimed, the outcome-prediction result, what the top outputs look like before and after brief
optimization, and for an LLM judge its human agreement, its bias tests and its recorded version.
State plainly whether the metric is validated, and for what use.
