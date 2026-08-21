# Environments

Describes specifics required to run experiments on different compute infrastructure.
Per-repo facts (interpreter, test runner, formatter) are not recorded here — they live in each
project's `CLAUDE.md`.

## laptop

Local development laptop (OSX, Metal).

| Fact | Value |
|---|---|
| Hardware | Apple M2 Max, 12 cores, 32 GB unified memory |
| OS | macOS 26.6.1 |
| GPU | Metal only — no CUDA. PyTorch uses the `mps` backend |
| Scheduler | None. Jobs run directly in the shell |
| Role | Smoke tests and development only. Full-scale runs go to a cluster |

Limitations:

- No CUDA. Code paths that require CUDA kernels do not run here.
- GPU memory is the same 32 GB unified pool the CPU uses. Large models do not fit.
- Some operations are not implemented on `mps`. A failure on `mps` is not proof the code is
  broken — confirm on a CUDA cluster before you debug it as a code defect.
- No scheduler, so jobs die when the laptop sleeps. Do not start long unattended runs.

Other environments (clusters) are added here from the systems themselves as they are used.
