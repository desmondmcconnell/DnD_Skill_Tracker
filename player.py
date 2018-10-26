"""
Player class for Dungeons and Dragons
"""

from skill import Skill
from attribute import Attribute
from item import Item


class Player:

    def __init__(self, name=""):
        self.name = name
        self.skills = []
        self.attributes = []
        self.items = []
        self.skill_to_index = {}
        self.index_counter = 0

    def __str__(self):
        return "{}, {}, {}".format(self.skills, self.attributes, self.items)

    def __repr__(self):
        return "{}".format(self.name)

    def load_player_skills(self, file_name):
        """Loads the player skills from the file"""
        file = open(file_name)
        for line in file:
            line = line.split(",")
            skill = Skill(line[0], int(line[1]), int(line[2].strip()))
            self.skills.append(skill)
            self.skill_to_index[skill.name] = self.index_counter
            self.index_counter += 1
        file.close()

    def load_player_attributes(self, file_name):
        """Loads the player attributes from the file"""
        file = open(file_name)
        for line in file:
            line = line.split(",")
            attribute = Attribute(line[0], line[1].strip())
            self.attributes.append(attribute)
        file.close()

    def save_player_skills(self, file_name):
        """Saves the player skills to the file"""
        file = open(file_name, "w")
        for skill in self.skills:
            print("{},{},{}".format(skill.name, skill.level, skill.chance_to_increase), file=file)
        file.close()

    def save_player_attributes(self, file_name):
        """Saves the player attributes to the file"""
        file = open(file_name, "w")
        for attribute in self.attributes:
            print("{},{}".format(attribute.name, attribute.quality), file=file)
        file.close()

    def load_player_items(self, file_name):
        """Loads the player attributes from the file"""
        file = open(file_name)
        for line in file:
            line = line.split(",")
            line[4] = line[4].replace("'", "").replace("[", "").replace("]", "").strip("\n")
            enabled = False if line[3] != "True" else True
            item = Item(line[0], line[1], int(line[2]), enabled)
            self.items.append(item)
            modifier = line[4]
            item.modifiers.append(modifier)
            item.load_skill_modifiers()
        file.close()

    def save_player_items(self, file_name):
        """Saves the player skills to the file"""
        file = open(file_name, "w")
        for item in self.items:
            print("{},{},{},{},{}".format(item.name, item.description, item.quantity, item.enabled,
                                          item.modifiers), file=file)
        file.close()
