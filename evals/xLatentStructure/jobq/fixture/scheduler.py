from report import label, status


def start(job):
    job.running = True
    job.attempts += 1


def finish(job, store, output):
    job.running = False
    job.done = True
    store.save(f"{job.name} {label(job.kind)} {status(job)}: {output}")


def fail(job):
    job.running = False
    job.failed = True


def retry(job, cfg):
    if job.attempts <= cfg.get("retries", 3):
        job.running = True
        job.attempts += 1
        return True
    return False


def cancel(job, queue):
    queue.drop(job)
