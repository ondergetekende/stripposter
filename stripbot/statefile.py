import json


class StateFile(dict):
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename) as fp:
                self.update(json.load(fp))
        except FileNotFoundError:
            # treat file not found as an empty statefile
            pass

    def save(self):
        with open(self.filename, 'w') as fp:
            json.dump(self, fp)

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        self.save()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.save()
