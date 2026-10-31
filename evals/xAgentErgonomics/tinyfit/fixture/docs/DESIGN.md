# tinyfit design

tinyfit fits a one-weight linear model to shards of synthetic data.

## Components

- `prep.py` splits the raw rows into shards.
- `train.py` fits the weight on all shards. The learning rate `lr` must be set in the config.
- `evaluate.py` scores the latest run. A run passes at an accuracy of at least 0.80.
- `configs/` holds one JSON file per experiment.

## Operation

Run `python status.py` to see the state of every run.

Train with `python train.py --config configs/base.json`.

## Results

Each run writes to `runs/<timestamp>/`.
