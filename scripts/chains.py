"""Generate CHAINS.md and the README figures from the skill-to-skill references in skills/*/SKILL.md.

    python3 scripts/chains.py          write CHAINS.md and the README block
    python3 scripts/chains.py --check  exit 1 if a reference is unclassified or either file is stale
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- chains:begin -->", "<!-- chains:end -->"

# alt: names an alternative. then: A calls or hands off to B. first: B runs before A.
REFERENCES = {
    ("xAgentErgonomics", "xAtomicConcepts"): "then",
    ("xAgentErgonomics", "xConfigHygiene"): "then",
    ("xAgentErgonomics", "xDebugHarness"): "then",
    ("xAgentErgonomics", "xDesignDebate"): "alt",
    ("xAgentErgonomics", "xDeslop"): "then",
    ("xAgentErgonomics", "xDocSweep"): "alt",
    ("xAgentErgonomics", "xExperimentPlan"): "then",
    ("xAgentErgonomics", "xRegressionGate"): "then",
    ("xAgentErgonomics", "xSpecDiff"): "alt",
    ("xAnalyzeLogs", "xCiTriage"): "alt",
    ("xAnalyzeLogs", "xPlotResults"): "alt",
    ("xAutonomousCampaign", "xExperimentPlan"): "first",
    ("xAutonomousCampaign", "xHandoff"): "then",
    ("xCiTriage", "xAnalyzeLogs"): "alt",
    ("xCiTriage", "xHypothesisDebug"): "then",
    ("xCleanBranch", "xShip"): "then",
    ("xColleagueReport", "xPlotResults"): "first",
    ("xColleagueReport", "xSanitize"): "then",
    ("xConfigHygiene", "xDeslop"): "then",
    ("xDeslop", "xAtomicConcepts"): "alt",
    ("xDocSweep", "xDeslop"): "alt",
    ("xDocSweep", "xHandoff"): "alt",
    ("xDocSweep", "xSpecDiff"): "alt",
    ("xDocSweep", "xWriteSte"): "alt",
    ("xExperimentPlan", "xDesignDebate"): "first",
    ("xFreshEyes", "xSpecDiff"): "alt",
    ("xHypothesisDebug", "xDebugHarness"): "then",
    ("xHypothesisDebug", "xMinimalRepro"): "then",
    ("xImplementPaper", "xSmokeThenScale"): "then",
    ("xLatentStructure", "xConfigHygiene"): "then",
    ("xLatentStructure", "xDesignDebate"): "then",
    ("xLatentStructure", "xHandoff"): "then",
    ("xLatentStructure", "xHypothesisDebug"): "then",
    ("xLatentStructure", "xLatentBugAudit"): "then",
    ("xLatentStructure", "xSubsystemSweep"): "then",
    ("xPlotResults", "xAnalyzeLogs"): "first",
    ("xRefAudit", "xLitGround"): "alt",
    ("xSpecDiff", "xFreshEyes"): "alt",
    ("xSubsystemSweep", "xDeslop"): "alt",
    ("xSubsystemSweep", "xLatentBugAudit"): "alt",
    ("xSubsystemSweep", "xRegressionGate"): "first",
    ("xSubsystemSweep", "xShip"): "then",
    ("xTriageReport", "xHypothesisDebug"): "then",
    ("xWriteSte", "xAtomicConcepts"): "then",
    ("xWriteSte", "xSpecDiff"): "then",
}

# S: stated in a SKILL.md. P: proposed, stated in no SKILL.md. "fix" is a code change, not a skill.
S, P = "S", "P"
WORKFLOWS = [
    ("Fix a defect", "From a report, a CI failure or a playtest list, to a shipped fix.", [
        (S, "xTriageReport", "xHypothesisDebug"), (S, "xCiTriage", "xHypothesisDebug"),
        (S, "xHypothesisDebug", "xDebugHarness"), (S, "xHypothesisDebug", "xMinimalRepro"),
        (P, "xHypothesisDebug", "fix"), (P, "fix", "xRegressionGate"), (P, "xRegressionGate", "xShip"),
        (P, "fix", "xCleanBranch"), (S, "xCleanBranch", "xShip")]),
    ("Structure audit to refactor", "xLatentStructure records go to the skill that acts on them.", [
        (S, "xLatentStructure", "xLatentBugAudit"), (S, "xLatentStructure", "xHypothesisDebug"),
        (S, "xLatentStructure", "xSubsystemSweep"), (S, "xLatentStructure", "xDesignDebate"),
        (S, "xLatentStructure", "xConfigHygiene"), (S, "xConfigHygiene", "xDeslop"),
        (S, "xRegressionGate", "xSubsystemSweep"), (S, "xSubsystemSweep", "xShip"),
        (P, "xDesignDebate", "xSubsystemSweep"), (P, "xLatentBugAudit", "xHypothesisDebug")]),
    ("Experiment lifecycle", "From a design question to a report for collaborators.", [
        (P, "xLitGround", "xDesignDebate"), (S, "xDesignDebate", "xExperimentPlan"),
        (P, "xMetricValidation", "xExperimentPlan"), (S, "xExperimentPlan", "xAutonomousCampaign"),
        (P, "xExperimentPlan", "xSmokeThenScale"), (S, "xAutonomousCampaign", "xHandoff"),
        (P, "xSmokeThenScale", "xAnalyzeLogs"), (P, "xAutonomousCampaign", "xAnalyzeLogs"),
        (S, "xAnalyzeLogs", "xPlotResults"), (S, "xPlotResults", "xColleagueReport"),
        (S, "xColleagueReport", "xSanitize")]),
    ("Paper to code", "Implement a published method and land it.", [
        (S, "xImplementPaper", "xSmokeThenScale"), (P, "xImplementPaper", "xSpecDiff"),
        (P, "xSpecDiff", "xFreshEyes"), (P, "xSmokeThenScale", "xShip")]),
    ("Write and submit a paper", "From figures to a submission.", [
        (P, "xPlotResults", "xWriteSte"), (S, "xWriteSte", "xAtomicConcepts"), (S, "xWriteSte", "xSpecDiff"),
        (P, "xLitGround", "xRefAudit"), (P, "xWriteSte", "xRefAudit"), (P, "xRefAudit", "xSanitize")]),
    ("Docs and agent ergonomics", "Tracking docs to a redesigned plan whose milestones each name a skill.", [
        (P, "xDocSweep", "xAgentErgonomics"), (S, "xAgentErgonomics", "xExperimentPlan"),
        (S, "xAgentErgonomics", "xConfigHygiene"), (S, "xAgentErgonomics", "xDebugHarness"),
        (S, "xAgentErgonomics", "xRegressionGate"), (S, "xAgentErgonomics", "xDeslop"),
        (S, "xAgentErgonomics", "xAtomicConcepts"), (S, "xConfigHygiene", "xDeslop")]),
]

KIND_LABEL = {"alt": "alternative", "then": "A then B", "first": "B before A"}
LEGEND = "`==>` stated in a SKILL.md · `-.->` proposed, in no SKILL.md · arrows run in execution order"


def scan(skills):
    found = {}
    for skill in skills:
        path = REPO / "skills" / skill / "SKILL.md"
        for number, line in enumerate(path.read_text().splitlines(), 1):
            for target in re.findall(r"\bx[A-Z][A-Za-z]+", line):
                if target != skill:
                    found.setdefault((skill, target), f"skills/{skill}/SKILL.md:{number}")
    return found


def problems(skills, found, steps):
    out = [f"unknown skill {b} at {site}" for (a, b), site in found.items() if b not in skills]
    out += [f"unclassified reference {a} -> {b} at {site}: add it to REFERENCES"
            for (a, b), site in found.items() if b in skills and (a, b) not in REFERENCES]
    out += [f"stale reference {a} -> {b}: no longer in skills/{a}/SKILL.md"
            for a, b in REFERENCES if (a, b) not in found]
    for name, _, edges in WORKFLOWS:
        for kind, a, b in edges:
            out += [f"{name}: {n} is not a skill" for n in (a, b) if n != "fix" and n not in skills]
            if (kind == S) != ((a, b) in steps):
                out.append(f"{name}: {a} -> {b} is drawn {'stated' if kind == S else 'proposed'} "
                           f"but is {'a' if (a, b) in steps else 'no'} stated chain step")
    return out


def mermaid(lines):
    return "```mermaid\nflowchart LR\n" + "\n".join("  " + line for line in lines) + "\n```"


def workflow_figure(edges):
    lines = [f"{a} {'==>' if kind == S else '-.->'} {b}" for kind, a, b in edges]
    if any("fix" in (a, b) for _, a, b in edges):
        lines = ['fix["code change<br/>(not a skill)"]:::nonskill'] + lines
        lines.append("classDef nonskill fill:none,stroke-dasharray:4 3")
    return mermaid(lines)


def workflows(level):
    blocks = []
    for name, blurb, edges in WORKFLOWS:
        stated = sum(kind == S for kind, _, _ in edges)
        blocks.append(f"{'#' * level} {name}\n\n{blurb} {stated} stated, {len(edges) - stated} proposed.\n\n"
                      f"{workflow_figure(edges)}")
    return "\n\n".join(blocks)


def chains_md(skills, found, steps):
    alternatives = sorted({tuple(sorted(pair)) for pair, kind in REFERENCES.items() if kind == "alt"})
    graph = [f"{a} ==> {b}" for a, b in sorted(steps)] + [f"{a} -. or .- {b}" for a, b in alternatives]
    linked = {n for pair in REFERENCES for n in pair}
    in_steps = {n for pair in steps for n in pair}
    in_workflows = {n for _, _, edges in WORKFLOWS for _, a, b in edges for n in (a, b)}
    rows = "\n".join(f"| {a} | {b} | {KIND_LABEL[REFERENCES[a, b]]} | `{found[a, b]}` |"
                     for a, b in sorted(REFERENCES))
    n_alt = sum(kind == "alt" for kind in REFERENCES.values())
    return f"""# Skill chains

Generated by `scripts/chains.py` from the skill-to-skill references in `skills/*/SKILL.md`. Edit
the script, not this file. `python3 scripts/chains.py --check` fails when this file or the README
figures are stale, or when a reference has no classification.

{LEGEND}.

{len(REFERENCES)} references: {n_alt} name an alternative, {len(REFERENCES) - n_alt} are chain steps.

## Workflows

{workflows(3)}

## All stated references

`-. or .-` joins alternatives.

{mermaid(graph)}

| Skills | |
|---|---|
| in no reference | {", ".join(s for s in skills if s not in linked) or "none"} |
| in no chain step | {", ".join(s for s in skills if s not in in_steps) or "none"} |
| in no workflow | {", ".join(s for s in skills if s not in in_workflows) or "none"} |

## References

| A | B | Kind | Site |
|---|---|---|---|
{rows}
"""


def readme_block():
    return (f"{BEGIN}\n## Skill chains\n\nSuggested chains of skills. {LEGEND}. Details and the full "
            f"reference graph: [CHAINS.md](CHAINS.md).\n\n{workflows(3)}\n{END}")


def main():
    check = sys.argv[1:] == ["--check"]
    skills = sorted(p.parent.name for p in (REPO / "skills").glob("x*/SKILL.md"))
    found = scan(skills)
    steps = {(b, a) if kind == "first" else (a, b) for (a, b), kind in REFERENCES.items() if kind != "alt"}
    errors = problems(skills, found, steps)
    readme = (REPO / "README.md").read_text()
    if readme.count(BEGIN) != 1 or readme.count(END) != 1:
        errors.append(f"README.md must hold {BEGIN} and {END} once each")
    if errors:
        sys.exit("\n".join(errors))
    start, stop = readme.index(BEGIN), readme.index(END) + len(END)
    outputs = {REPO / "CHAINS.md": chains_md(skills, found, steps),
               REPO / "README.md": readme[:start] + readme_block() + readme[stop:]}
    stale = [path.name for path, text in outputs.items() if not path.exists() or path.read_text() != text]
    if check:
        if stale:
            sys.exit(f"stale: {', '.join(stale)}; run python3 scripts/chains.py")
        return
    for path, text in outputs.items():
        path.write_text(text)
    print(f"wrote {', '.join(stale) or 'nothing (up to date)'}")


if __name__ == "__main__":
    main()
