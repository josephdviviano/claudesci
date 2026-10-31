# Grading key — tinyfit

Validated by validate.py: on the pristine fixture every outcome grader fails and every
preservation grader passes; on `solution/` every grader passes; on a code-edited copy every
preservation grader fails.

## Planted defects

| ID | Defect | Site | Fixed when | Grader |
|---|---|---|---|---|
| P1 | Planned command shown as real | DESIGN.md: "Run `python status.py`"; no status.py exists | Every line naming status.py says planned | status-planned-* |
| P2 | Two names for one concept | Docs say shard; code, config and logs say chunk | Every doc line with shard also names chunk | one-name-* |
| P3 | Silent default | train.py `cfg.get("lr", 0.1)`; DESIGN.md says lr is required | Plan names the lr default | plan-lr |
| P4 | Cost only in a code comment | train.py: full run about 75 s (measured) | DESIGN.md states the cost | cost-stated (llm) |
| P5 | Cheap check undocumented | train.py `--steps` | DESIGN.md names `--steps` | smoke-documented |
| P6 | One fact, two values | DESIGN.md threshold 0.80; evaluate.py 0.85. The recorded run scored 0.812: FAIL by the code, PASS by the doc | DESIGN.md does not present 0.80 as current | threshold-one-home (llm) |
| P7 | Map links one doc | CLAUDE.md does not link the plan | CLAUDE.md links PLAN.FIT.md | map-links-plan |
| P8 | No observe command | No way to list runs | Plan has a status milestone | plan-status |
| P9 | Milestones without acceptance | PLAN.FIT.md M0–M2 | Each milestone has a done check | plan-acceptance (llm) |

## Preservation

| Grader | Fails when |
|---|---|
| no-new-code | Any `.py` file is created |
| code-lr-kept, code-threshold-kept, code-chunk-kept | The planted code line changes |
| design-kept, plan-kept | The document is deleted or emptied |
| status-planned-map (guard) | The run adds an unmarked `status.py` to CLAUDE.md |

## Fixture facts

The fixture is consistent with itself. `prep.py` gives accuracy ≈ 0.81 for any step count, between
the two thresholds. `runs/2026-10-01T10-00-00` is a real full run of `configs/base.json`;
`evaluate.py` reproduces its `eval.log` after `prep.py`. The plan is in `plans/` because the
eval sandbox blocks writes to `.claude/`.

## Not checked by validate.py

The llm graders: cost-stated, threshold-one-home, plan-acceptance, and `measured` (final
message: before/after grades from cold-start agents).
