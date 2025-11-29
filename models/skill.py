"""Simple skill model (placeholder)."""

class Skill:
    def __init__(self, key: str, cooldown: float, cast_time: float, priority: int):
        self.key = key
        self.cooldown = cooldown
        self.cast_time = cast_time
        self.priority = priority

    def to_dict(self):
        return {
            "key": self.key,
            "cooldown": self.cooldown,
            "cast_time": self.cast_time,
            "priority": self.priority,
        }
