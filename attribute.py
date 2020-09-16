""" The attributes that define any player"""


class Attribute:

    def __init__(self, name="", quality=""):
        self.name = name
        self.quality = quality

    def __str__(self):
        return "{}: {}".format(self.name, self.quality)

    def __repr__(self):
        return "{}: {}".format(self.name, self.quality)
