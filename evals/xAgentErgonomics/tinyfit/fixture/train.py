import argparse
import json
import pathlib
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--data", default="data")
    parser.add_argument("--steps", type=int)
    args = parser.parse_args()
    cfg = json.loads(pathlib.Path(args.config).read_text())
    lr = cfg.get("lr", 0.1)
    # A full run takes about 75 s on one core.
    steps = args.steps or cfg["steps"]
    rows = []
    for path in sorted(pathlib.Path(args.data).glob("chunk_*.json")):
        rows += json.loads(path.read_text())
    w = 0.0
    for step in range(steps):
        x, y = rows[step % len(rows)]
        w -= lr * (w * x - y) * x
    run = pathlib.Path("runs") / time.strftime("%Y-%m-%dT%H-%M-%S")
    run.mkdir(parents=True)
    (run / "model.json").write_text(json.dumps({"w": w}))
    print(f"saved {run}")


if __name__ == "__main__":
    main()
