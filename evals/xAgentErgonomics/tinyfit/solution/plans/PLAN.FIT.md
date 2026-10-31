# PLAN.FIT

M0. Remove the silent `lr` default in `train.py` (`xConfigHygiene`). Done when a config without
    `lr` fails at start.
M1. Add `status.py`: one line per run with config, steps and accuracy. Done when it lists
    `runs/2026-10-01T10-00-00`.
M2. Evaluate the base model. Done when `python evaluate.py` prints one line for the M1 run.
