import fnmatch
import pathlib
import re
import shutil
import sys
import tempfile

import yaml

CASE = pathlib.Path(__file__).parent
PRESERVATION = {"no-new-code", "code-lr-kept", "code-threshold-kept", "code-chunk-kept",
                "design-kept", "plan-kept"}
# Pass on the pristine fixture; fail only if a run introduces the defect.
GUARDS = {"status-planned-map"}
FLAGS = {"m": re.M, "i": re.I, "s": re.S}

CODE_EDITS = [
    ("train.py", 'cfg.get("lr", 0.1)', 'cfg["lr"]'),
    ("evaluate.py", "THRESHOLD = 0.85", "THRESHOLD = 0.80"),
    ("prep.py", 'cfg["chunk_size"]', 'cfg["shard_size"]'),
]
DOC_DAMAGE = {
    "docs/DESIGN.md": "",
    "plans/PLAN.FIT.md": None,
    "CLAUDE.md": "# tinyfit\n\nRun `python status.py` first.\n",
}


def grade(grader, workspace, created):
    if grader["type"] == "file_exists":
        found = any(fnmatch.fnmatch(path, grader["path"]) or
                    fnmatch.fnmatch(path, grader["path"].removeprefix("**/")) for path in created)
        return found == grader.get("exists", True)
    path = workspace / grader["target"]["path"]
    if not path.exists():
        return False
    flags = 0
    for letter in grader.get("flags", ""):
        flags |= FLAGS[letter]
    hit = re.search(grader["pattern"], path.read_text(), flags) is not None
    return hit if grader.get("match", "contains") == "contains" else not hit


def workspace(tmp, name, overlay, code_edits, doc_damage):
    root = pathlib.Path(tmp) / name
    shutil.copytree(CASE / "fixture", root)
    if overlay:
        shutil.copytree(CASE / "solution", root, dirs_exist_ok=True)
    for file, old, new in code_edits:
        text = (root / file).read_text()
        assert old in text, f"{file}: {old!r} not found"
        (root / file).write_text(text.replace(old, new))
    for file, text in doc_damage.items():
        if text is None:
            (root / file).unlink()
        else:
            (root / file).write_text(text)
    return root


def main():
    graders = [g for g in yaml.safe_load((CASE / "case.yaml").read_text())["graders"]
               if g["type"] in ("regex", "file_exists")]
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        kept = PRESERVATION | GUARDS
        scenarios = [
            ("pristine", workspace(tmp, "pristine", False, [], {}), [],
             {g["name"]: g["name"] in kept for g in graders}),
            ("solution", workspace(tmp, "solution", True, [], {}), [],
             {g["name"]: True for g in graders}),
            ("broken", workspace(tmp, "broken", True, CODE_EDITS, DOC_DAMAGE), ["status.py"],
             {name: False for name in kept}),
        ]
        for label, root, created, expected in scenarios:
            for grader in graders:
                if grader["name"] not in expected:
                    continue
                passed = grade(grader, root, created)
                ok = passed == expected[grader["name"]]
                failures += not ok
                print(f"{'ok  ' if ok else 'FAIL'} {label:12} {grader['name']:24} "
                      f"{'pass' if passed else 'fail'}")
    print(f"{failures} unexpected")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
