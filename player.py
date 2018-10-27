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
        self.previous_attributes = []
        self.items = []
        self.skill_to_index = {}
        self.skill_index_counter = 0
        self.attribute_to_index = {}
        self.attribute_index_counter = 0

    def __str__(self):
        return "{}, {}, {}".format(self.skills, self.attributes, self.items)

    def __repr__(self):
        return "{}".format(self.name)

    def load_player_skills(self, file_name):
        """Loads the player skills from the file"""
        self.skills = []
        self.skill_index_counter = 0
        file = open(file_name)
        for line in file:
            line = line.split(",")
            skill = Skill(line[0], int(line[1]), int(line[2].strip()))
            self.skills.append(skill)
            self.skill_to_index[skill.name] = self.skill_index_counter
            self.skill_index_counter += 1
        file.close()

    def load_player_attributes(self, file_name):
        """Loads the player attributes from the file"""
        self.attributes = []
        self.attribute_index_counter = 0
        file = open(file_name)
        for line in file:
            line = line.split(",")
            attribute = Attribute(line[0], line[1].strip())
            self.attributes.append(attribute)
            self.attribute_to_index[attribute.name] = self.attribute_index_counter
            self.attribute_index_counter += 1
        file.close()

    def load_player_previous_attributes(self, file_name):
        """Loads the player attributes from the file"""
        file = open(file_name)
        for line in file:
            line = line.split(",")
            attribute = Attribute(line[0], line[1].strip())
            self.previous_attributes.append(attribute)
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

    def save_player_prev_att(self, file_name):
        """Saves the player attributes to the file"""
        file = open(file_name, "w")
        for attribute in self.previous_attributes:
            print("{},{}".format(attribute.name, attribute.quality), file=file)
        file.close()

    def load_player_items(self, file_name):
        """Loads the player attributes from the file"""
        file = open(file_name)
        for line in file:
            line = line.split(",")
            line[5] = line[5].replace("'", "").replace("[", "").replace("]", "")
            line[6] = line[6].replace("'", "").replace("[", "").replace("]", "").strip("\n")
            enabled = False if line[4] != "True" else True
            item = Item(line[0], line[1], int(line[2]), float(line[3]), enabled)
            self.items.append(item)
            skill_modifier = line[5]
            attribute_modifier = line[6]
            item.skill_modifiers.append(skill_modifier)
            item.attribute_modifiers.append(attribute_modifier)
            item.load_attribute_modifiers()
            item.load_skill_modifiers()
        file.close()

    def save_player_items(self, file_name):
        """Saves the player skills to the file"""
        file = open(file_name, "w")
        for item in self.items:
            print("{},{},{},{},{},{},{}".format(item.name, item.description, item.quantity, item.weight, item.enabled,
                                                item.skill_modifiers, item.attribute_modifiers), file=file)
        file.close()
