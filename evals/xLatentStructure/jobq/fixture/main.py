import json

from job import Job
from jobqueue import Queue
from runner import VERBOSE, run
from scheduler import cancel, fail, finish, retry, start
from store import Store

JOBS = [("a", "train"), ("b", "eval"), ("c", "export"), ("d", "train")]


def process(job, cfg, store):
    start(job)
    while True:
        try:
            output = run(job)
        except RuntimeError:
            fail(job)
            if retry(job, cfg):
                continue
            return
        finish(job, store, output)
        return


def main():
    with open("config.json") as f:
        cfg = json.load(f)
    queue = Queue()
    store = Store()
    for name, kind in JOBS:
        queue.push(Job(name, kind))
    cancel(queue.items[-1], queue)
    while queue.items:
        process(queue.pop(), cfg, store)
    store.open(cfg["store"])
    store.save(f"summary pending={queue.n_pending}")
    if VERBOSE:
        print("done")


if __name__ == "__main__":
    main()
