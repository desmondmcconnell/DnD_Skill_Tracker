"""
Player class for Dungeons and Dragons
"""

from skill import Skill


class Player:

    def __init__(self, name=""):
        self.name = name
        self.skills = []

    def __str__(self):
        return "{}".format(self.skills)

    def __repr__(self):
        return "{}".format(self.name)

    def load_player(self, file_name):
        """Loads the player skills from the file"""
        file = open(file_name)
        for line in file:
            line = line.split(",")
            skill = Skill(line[0], int(line[1]), int(line[2].strip()))
            self.skills.append(skill)
        file.close()

    def save_player(self, file_name):
        """Saves the player skills to the file"""
        file = open(file_name, "w")
        for skill in self.skills:
            print("{},{},{}".format(skill.name, skill.level, skill.chance_to_increase), file=file)
        file.close()
