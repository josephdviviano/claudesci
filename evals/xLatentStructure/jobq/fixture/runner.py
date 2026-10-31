import sys

VERBOSE = "-v" in sys.argv


def run_train(job):
    return f"trained {job.name}"


def run_eval(job):
    if job.attempts == 1:
        raise RuntimeError("cold cache")
    return f"evaluated {job.name}"


def run_export(job):
    return f"exported {job.name}"


HANDLERS = {"train": run_train, "eval": run_eval}


def run(job):
    if VERBOSE:
        print(f"run {job.name}")
    return HANDLERS.get(job.kind, run_train)(job)
