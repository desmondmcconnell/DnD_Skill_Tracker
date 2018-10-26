from attribute import Attribute
from skill import Skill
# from player import Player


class Item:

    def __init__(self, name="", description="", quantity=1, enabled=False):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.enabled = enabled
        self.modifiers = []
        self.skills_container = []
        self.skills = []
        self.skill_index = 0
        self.skill_to_index = {}

    def __str__(self):
        return "{}, {}, {} (Modifies: {})".format(self.name, self.description, self.quantity, self.modifiers)

    def __repr__(self):
        return "{}, {}, {} (Modifies: {})".format(self.name, self.description, self.quantity, self.modifiers)

    def load_skill_modifiers(self):
        for modifier in self.modifiers:
            modifier = modifier.split(";")
            for i in range(len(modifier)):
                self.skills_container.append(modifier[i])
        for i, skill in enumerate(self.skills_container, 0):
            if i % 2 == 0:
                name = skill
            else:
                level = int(skill)
                new_skill = Skill(name, level)
                self.skills.append(new_skill)
        self.skills_container = []

    def update_skill_modifiers(self):
        self.skills = []
        for modifier in self.modifiers:
            modifier = modifier.split(";")
            for i in range(len(modifier)):
                self.skills_container.append(modifier[i])
        for i, skill in enumerate(self.skills_container, 0):
            if i % 2 == 0:
                name = skill
            else:
                level = int(skill)
                new_skill = Skill(name, level)
                self.skills.append(new_skill)
        self.skills_container = []

    def switch_enabled(self):
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True

