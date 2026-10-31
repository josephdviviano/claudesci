class Store:
    def __init__(self):
        self.path = None

    def open(self, path):
        self.path = path

    def save(self, line):
        with open(self.path or "default.log", "a") as f:
            f.write(line + "\n")
