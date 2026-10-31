class Job:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
        self.running = False
        self.done = False
        self.failed = False
        self.attempts = 0
