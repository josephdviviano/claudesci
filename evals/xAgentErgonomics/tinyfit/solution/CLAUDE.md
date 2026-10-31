# tinyfit

Fits a one-weight linear model to chunks of synthetic data.

| Layer | Doc | Run first |
|---|---|---|
| Data, train, evaluate | docs/DESIGN.md | `python train.py --config configs/base.json --steps 100` (smoke, seconds) |
| Open work | plans/PLAN.FIT.md | |

## Traps
- `evaluate.py` scores the newest directory in `runs/`, not a run you name.

## Where knowledge goes
| Knowledge | Destination |
|---|---|
| Decision and reason | docs/DESIGN.md, decision log |
| Trap | Traps, above |
