"""
Player class for Dungeons and Dragons
"""

from skill import Skill
from attribute import Attribute


class Player:

    def __init__(self, name=""):
        self.name = name
        self.skills = []
        self.attributes = []
        self.items = []

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
