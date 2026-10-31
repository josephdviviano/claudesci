# tinyfit design

tinyfit fits a one-weight linear model to chunks of synthetic data.

| Layer | Contract | Observe | Act | Verify | Cost |
|---|---|---|---|---|---|
| Data | config → `data/chunk_NNN.json`, `chunk_size` rows each | `ls data` | `python prep.py --config C` | chunk count is rows / chunk_size | seconds |
| Train | chunks + config → `runs/<timestamp>/model.json` | `python status.py`, planned (M1) | `python train.py --config C` | `--steps 100` smoke | full run about 75 s on one core |
| Evaluate | newest run → accuracy; PASS at `THRESHOLD` in `evaluate.py` | `python evaluate.py` | | | seconds |

`lr` has a silent default of 0.1 in `train.py`. Its removal is planned (M0).

## Decision log
