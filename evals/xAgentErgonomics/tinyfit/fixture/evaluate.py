import json
import pathlib

THRESHOLD = 0.85


def main():
    run = sorted(pathlib.Path("runs").iterdir())[-1]
    w = json.loads((run / "model.json").read_text())["w"]
    rows = []
    for path in sorted(pathlib.Path("data").glob("chunk_*.json")):
        rows += json.loads(path.read_text())
    accuracy = sum(abs(w * x - y) < 0.5 for x, y in rows) / len(rows)
    verdict = "PASS" if accuracy >= THRESHOLD else "FAIL"
    print(f"{run.name} accuracy={accuracy:.3f} {verdict}")


if __name__ == "__main__":
    main()
