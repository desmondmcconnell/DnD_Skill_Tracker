from skill import Skill
from attribute import Attribute


class Item:

    def __init__(self, name="", description="", quantity=1, weight=0, enabled=False):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.weight = weight
        self.enabled = enabled
        self.skill_modifiers = []
        self.skills_container = []
        self.skills = []
        self.attribute_modifiers = []
        self.attributes_container = []
        self.attributes = []

    def __str__(self):
        return "{}, {}, {}, {} (Modifies: {}, {})".format(self.name, self.description, self.quantity, self.weight,
                                                          self.skill_modifiers, self.attribute_modifiers)

    def __repr__(self):
        return "{}, {}, {}, {} (Modifies: {}, {})".format(self.name, self.description, self.quantity, self.weight,
                                                          self.skill_modifiers, self.attribute_modifiers)

    def load_skill_modifiers(self):
        for modifier in self.skill_modifiers:
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
        self.load_skill_modifiers()

    def load_attribute_modifiers(self):
        for modifier in self.attribute_modifiers:
            modifier = modifier.split(";")
            for i in range(len(modifier)):
                self.attributes_container.append(modifier[i])
        for i, attribute in enumerate(self.attributes_container, 0):
            if i % 2 == 0:
                name = attribute
            else:
                quality = attribute
                new_attribute = Attribute(name, quality)
                self.attributes.append(new_attribute)
        self.attributes_container = []

    def update_attribute_modifiers(self):
        self.attributes = []
        self.load_attribute_modifiers()

    def switch_enabled(self):
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True
