claudesci
---------

Skills and workflows for R&D.

<!-- chains:begin -->
## Skill chains

Suggested chains of skills. `==>` stated in a SKILL.md · `-.->` proposed, in no SKILL.md · arrows run in execution order. Details and the full reference graph: [CHAINS.md](CHAINS.md).

### Fix a defect

From a report, a CI failure or a playtest list, to a shipped fix. 5 stated, 4 proposed.

```mermaid
flowchart LR
  fix["code change<br/>(not a skill)"]:::nonskill
  xTriageReport ==> xHypothesisDebug
  xCiTriage ==> xHypothesisDebug
  xHypothesisDebug ==> xDebugHarness
  xHypothesisDebug ==> xMinimalRepro
  xHypothesisDebug -.-> fix
  fix -.-> xRegressionGate
  xRegressionGate -.-> xShip
  fix -.-> xCleanBranch
  xCleanBranch ==> xShip
  classDef nonskill fill:none,stroke-dasharray:4 3
```

### Structure audit to refactor

xLatentStructure records go to the skill that acts on them. 8 stated, 2 proposed.

```mermaid
flowchart LR
  xLatentStructure ==> xLatentBugAudit
  xLatentStructure ==> xHypothesisDebug
  xLatentStructure ==> xSubsystemSweep
  xLatentStructure ==> xDesignDebate
  xLatentStructure ==> xConfigHygiene
  xConfigHygiene ==> xDeslop
  xRegressionGate ==> xSubsystemSweep
  xSubsystemSweep ==> xShip
  xDesignDebate -.-> xSubsystemSweep
  xLatentBugAudit -.-> xHypothesisDebug
```

### Experiment lifecycle

From a design question to a report for collaborators. 6 stated, 5 proposed.

```mermaid
flowchart LR
  xLitGround -.-> xDesignDebate
  xDesignDebate ==> xExperimentPlan
  xMetricValidation -.-> xExperimentPlan
  xExperimentPlan ==> xAutonomousCampaign
  xExperimentPlan -.-> xSmokeThenScale
  xAutonomousCampaign ==> xHandoff
  xSmokeThenScale -.-> xAnalyzeLogs
  xAutonomousCampaign -.-> xAnalyzeLogs
  xAnalyzeLogs ==> xPlotResults
  xPlotResults ==> xColleagueReport
  xColleagueReport ==> xSanitize
```

### Paper to code

Implement a published method and land it. 1 stated, 3 proposed.

```mermaid
flowchart LR
  xImplementPaper ==> xSmokeThenScale
  xImplementPaper -.-> xSpecDiff
  xSpecDiff -.-> xFreshEyes
  xSmokeThenScale -.-> xShip
```

### Write and submit a paper

From figures to a submission. 2 stated, 4 proposed.

```mermaid
flowchart LR
  xPlotResults -.-> xWriteSte
  xWriteSte ==> xAtomicConcepts
  xWriteSte ==> xSpecDiff
  xLitGround -.-> xRefAudit
  xWriteSte -.-> xRefAudit
  xRefAudit -.-> xSanitize
```

### Docs and agent ergonomics

Tracking docs to a redesigned plan whose milestones each name a skill. 7 stated, 1 proposed.

```mermaid
flowchart LR
  xDocSweep -.-> xAgentErgonomics
  xAgentErgonomics ==> xExperimentPlan
  xAgentErgonomics ==> xConfigHygiene
  xAgentErgonomics ==> xDebugHarness
  xAgentErgonomics ==> xRegressionGate
  xAgentErgonomics ==> xDeslop
  xAgentErgonomics ==> xAtomicConcepts
  xConfigHygiene ==> xDeslop
```
<!-- chains:end -->
