"""Skills used by Dungeons and Dragons Players"""


class Skill:

    def __init__(self, name="", level=0, chance_to_increase=0):
        self.name = name
        self.level = level
        self.chance_to_increase = chance_to_increase

    def increase_level(self):
        """Increases the level of the skill"""
        if self.chance_to_increase > 100:
            self.level += 1

    def __str__(self):
        return "{}: {}, {}%".format(self.name, self.level, self.chance_to_increase)

    def __repr__(self):
        return "{}: {}, {}%".format(self.name, self.level, self.chance_to_increase)
