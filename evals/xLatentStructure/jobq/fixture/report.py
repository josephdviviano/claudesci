def status(job):
    if job.failed:
        return "failed"
    if job.done:
        return "done"
    if job.running:
        return "running"
    return "queued"


def label(kind):
    return {"train": "Training", "eval": "Evaluation", "export": "Export"}[kind]
