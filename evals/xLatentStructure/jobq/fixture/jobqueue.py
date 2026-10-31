class Queue:
    def __init__(self):
        self.items = []
        self.n_pending = 0

    def push(self, job):
        self.items.append(job)
        self.n_pending += 1

    def pop(self):
        self.n_pending -= 1
        return self.items.pop(0)

    def drop(self, job):
        self.items.remove(job)
