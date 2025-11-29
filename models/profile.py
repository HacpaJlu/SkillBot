"""Simple profile model (placeholder)."""

class Profile:
    def __init__(self, name: str, data: dict = None):
        self.name = name
        self.data = data or {}

    def to_dict(self):
        return {"name": self.name, **self.data}
