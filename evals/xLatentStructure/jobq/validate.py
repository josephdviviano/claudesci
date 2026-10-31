import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

CASE = pathlib.Path(__file__).parent
FLAGS = {"m": re.M, "i": re.I, "s": re.S}

FIXES = {
    "P1": ("scheduler.py", "        job.running = True\n        job.attempts += 1\n        return True",
           "        job.failed = False\n        job.running = True\n        job.attempts += 1\n        return True"),
    "P2": ("runner.py", '{"train": run_train, "eval": run_eval}',
           '{"train": run_train, "eval": run_eval, "export": run_export}'),
    "P3": ("main.py", '    while queue.items:\n        process(queue.pop(), cfg, store)\n    store.open(cfg["store"])\n',
           '    store.open(cfg["store"])\n    while queue.items:\n        process(queue.pop(), cfg, store)\n'),
    "P4": ("scheduler.py", 'cfg.get("retries", 3)', 'cfg["max_retries"]'),
    "P5": ("jobqueue.py", "        self.items.remove(job)", "        self.items.remove(job)\n        self.n_pending -= 1"),
}
KEPT = {"P1": "kept-retry-flags", "P2": "kept-handlers", "P3": "kept-store-order",
        "P4": "kept-retry-key", "P5": "kept-drop"}
REPORT = {"report-written", "sites-cited", "recount-given", "diagram-given"}

WITNESSES = {
    "P1": "from job import Job; from scheduler import *; from store import Store; from report import status\n"
          "j = Job('b', 'eval'); start(j); fail(j); retry(j, {'max_retries': 2})\n"
          "finish(j, Store(), 'x'); print(status(j) == 'failed')",
    "P2": "from job import Job; from runner import run; print(run(Job('c', 'export')) == 'trained c')",
    "P3": "import main, pathlib; main.main(); print(pathlib.Path('default.log').exists())",
    "P4": "from job import Job; from scheduler import retry\n"
          "j = Job('b', 'eval'); j.attempts = 3; print(retry(j, {'max_retries': 2}))",
    "P5": "from job import Job; from jobqueue import Queue\n"
          "q = Queue(); a, b = Job('a', 'train'), Job('b', 'train'); q.push(a); q.push(b); q.drop(b)\n"
          "print(q.n_pending != len(q.items))",
}


def manifests(root, plant):
    work = pathlib.Path(tempfile.mkdtemp())
    shutil.copytree(root, work, dirs_exist_ok=True)
    out = subprocess.run([sys.executable, "-c", WITNESSES[plant]], cwd=work, capture_output=True,
                         text=True, timeout=30)
    if out.returncode:
        sys.exit(f"{plant} witness crashed:\n{out.stderr}")
    return out.stdout.strip().splitlines()[-1] == "True"


def grade(grader, root):
    path = root / grader["target"]["path"]
    if not path.exists():
        return False
    flags = 0
    for letter in grader.get("flags", ""):
        flags |= FLAGS[letter]
    hit = re.search(grader["pattern"], path.read_text(), flags) is not None
    return hit if grader.get("match", "contains") == "contains" else not hit


def workspace(tmp, name, fixes, report):
    root = pathlib.Path(tmp) / name
    shutil.copytree(CASE / "fixture", root)
    if report:
        shutil.copy(CASE / "solution" / "LATENT.md", root / "LATENT.md")
    for plant in fixes:
        file, old, new = FIXES[plant]
        text = (root / file).read_text()
        assert text.count(old) == 1, f"{plant}: {old!r} not found once in {file}"
        (root / file).write_text(text.replace(old, new))
    return root


def main():
    graders = {g["name"]: g for g in yaml.safe_load((CASE / "case.yaml").read_text())["graders"]
               if g["type"] == "regex"}
    failures = 0

    def check(label, name, got, want):
        nonlocal failures
        ok = got == want
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {label:10} {name:18} {got}")

    with tempfile.TemporaryDirectory() as tmp:
        pristine = workspace(tmp, "pristine", [], False)
        for plant in FIXES:
            check("pristine", f"{plant} manifests", manifests(pristine, plant), True)
        for name, grader in graders.items():
            check("pristine", name, grade(grader, pristine), name not in REPORT)
        for plant in FIXES:
            fixed = workspace(tmp, f"fix-{plant}", [plant], False)
            for other in FIXES:
                check(f"fix-{plant}", f"{other} manifests", manifests(fixed, other), other != plant)
            for kept_plant, name in KEPT.items():
                check(f"fix-{plant}", name, grade(graders[name], fixed), kept_plant != plant)
        solution = workspace(tmp, "solution", [], True)
        for name, grader in graders.items():
            check("solution", name, grade(grader, solution), True)
    print(f"{failures} unexpected")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
