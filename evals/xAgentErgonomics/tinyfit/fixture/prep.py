import argparse
import json
import pathlib
import random


def main():
    parser = argparse.ArgumentParser(description="Split the raw rows into chunks.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", default="data")
    args = parser.parse_args()
    cfg = json.loads(pathlib.Path(args.config).read_text())
    rng = random.Random(cfg["seed"])
    rows = []
    for _ in range(cfg["rows"]):
        x = rng.random()
        rows.append((x, 0.6 * x + rng.gauss(0, 0.36)))
    out = pathlib.Path(args.out)
    out.mkdir(exist_ok=True)
    size = cfg["chunk_size"]
    for start in range(0, len(rows), size):
        index = start // size
        (out / f"chunk_{index:03d}.json").write_text(json.dumps(rows[start:start + size]))
        print(f"wrote chunk {index}")


if __name__ == "__main__":
    main()
