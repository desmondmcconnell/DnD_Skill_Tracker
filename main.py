"""
Dungeons and Dragons Skill Tracker for Multiple Players
Author: Desmond McConnell

URL: https://github.com/desmondmcconnell/DnD_Skill_Tracker
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from player import Player
from random import randint
import os

DEFAULT_TEXT = "Press 'Enter' In Text Box To Apply New Properties"
DEFAULT_FILE = "DEFAULT_PLAYER"
BOXES = (1, 2, 3, 4, 5)


class DndSkillTracker(App):
    label_text = StringProperty()
    status_text = StringProperty()

    def __init__(self, **kwargs):
        """Constructor method"""
        super().__init__(**kwargs)
        self.current_player = False
        self.page_counter = 1
        self.player_to_index = {}
        self.player_skills_to_filename = {}
        self.player_attributes_to_filename = {}
        self.players = []
        self.skill_index_start = 0
        self.attribute_index_start = 0
        self.player_number = 0

    def build(self):
        """Build the Kivy app from the .kv file"""
        self.status_text = "Press 'Enter' In Text Box To Apply New Levels"
        self.update_title()
        self.root = Builder.load_file('gui.kv')
        os.chdir('Players')
        self.walk()
        self.root.ids.player_selector.values = self.player_to_index.keys()
        self.root.ids.content_selector.values = ("Skills", "Attributes")
        return self.root

    def handle_next(self):
        """Displays the next set of skill widgets"""
        if self.root.ids.content_selector.text == "Skills":
            if self.page_counter == 11:
                return
            if self.current_player:
                self.clear_widget(DEFAULT_TEXT)
                self.page_counter += 1
                self.update_title()
                self.skill_index_start += 5
                self.create_skills_widgets()
            else:
                return
        else:
            if self.page_counter == 3:
                return
            if self.current_player:
                self.clear_widget(DEFAULT_TEXT)
                self.page_counter += 1
                self.update_title()
                self.attribute_index_start += 5
                self.create_attributes_widgets()

    def handle_previous(self):
        """Displays the previous set of skill widgets"""
        if self.page_counter == 1:
            return
        if self.root.ids.content_selector.text == "Skills":
            self.page_counter -= 1
            self.update_title()
            self.clear_widget(DEFAULT_TEXT)
            self.skill_index_start -= 5
            self.create_skills_widgets()
        else:
            self.page_counter -= 1
            self.update_title()
            self.clear_widget(DEFAULT_TEXT)
            self.attribute_index_start -= 5
            self.create_attributes_widgets()

    def character_swap(self, player):
        """Changes the current character and resets all things accordingly"""
        self.page_counter = 1
        self.update_title()
        try:
            player_index = self.player_to_index[player]
            self.current_player = self.players[player_index]
            self.skill_index_start = 0
            if self.root.ids.content_selector.text == "Skills":
                self.clear_widget(DEFAULT_TEXT)
                self.create_skills_widgets()
            else:
                self.root.ids.content_selector.text = "Skills"
        except KeyError:
            return

    def create_skills_widgets(self):
        for i, box in enumerate(BOXES, self.skill_index_start):
            self.create_skills(box, i)

    def update_title(self):
        """Updates the title of the app"""
        self.title = "Dungeons and Dragons Skill Tracker Page {}".format(self.page_counter)

    def walk(self):
        """Process all subdirectories using os.walk()."""
        for directory_name, subdirectories, file_names in os.walk('.'):
            for file in file_names:
                if DEFAULT_FILE in file:
                    continue
                self.add_player_data(file)

    def add_player_data(self, file):
        """Adds player to the player list from the file"""
        player_name = self.get_player_name(file)
        if player_name not in self.player_to_index:
            player = Player(player_name)
        else:
            player = self.players[self.player_to_index[player_name]]
        if "_1" in file:
            player.load_player_attributes(file)
            self.player_attributes_to_filename[player_name] = file
        else:
            player.load_player_skills(file)
            self.players.append(player)
            self.player_skills_to_filename[player_name] = file
            self.player_to_index[player_name] = self.player_number
            self.player_number += 1

    def get_player_name(self, file_name):
        """Gets the player name out of the file name"""
        player = ""
        marker = ""
        for character in file_name:
            if character != ".":
                if marker == ".":
                    continue
                player += character
            else:
                marker = character
                continue
        player = player.replace("_1", "").replace("_2", "")
        return player

    def clear_widget(self, text):
        """Deletes all the dynamic widgets"""
        for box in BOXES:
            self.root.ids["box_{}".format(box)].clear_widgets()
        self.status_text = text

    def handle_pass_button(self, instance):
        """Adds 10% to level chance on successful skill use"""
        id_number = instance.id.split("_")
        id_number = int(id_number[1])
        box = BOXES[id_number % 5]
        current_skill = self.current_player.skills[id_number]
        if current_skill.chance_to_increase < 100:
            current_skill.chance_to_increase += 10
        if current_skill.chance_to_increase > 100:
            current_skill.chance_to_increase = 100
        self.root.ids["box_{}".format(box)].clear_widgets()
        self.create_skills(box, id_number)
        self.status_text = "{} Roll Succeeded. 10% Added to Level Up Chance".format(current_skill.name)
        self.current_player.save_player_skills(self.player_skills_to_filename[self.current_player.name])

    def handle_fail_button(self, instance):
        """Adds 5% to level chance on failed skill use"""
        id_number = instance.id.split("_")
        id_number = int(id_number[1])
        box = BOXES[id_number % 5]
        current_skill = self.current_player.skills[id_number]
        if current_skill.chance_to_increase < 100:
            current_skill.chance_to_increase += 5
        self.root.ids["box_{}".format(box)].clear_widgets()
        self.create_skills(box, id_number)
        self.status_text = "{} Roll Failed. 5% Added to Level Up Chance".format(current_skill.name)
        self.current_player.save_player_skills(self.player_skills_to_filename[self.current_player.name])

    def create_skills(self, box, id_number):
        """Adds the labels, text input and buttons for the skills in the range"""
        try:
            current_skill = self.current_player.skills[id_number]
            if current_skill.name == "SPARE":
                name_object = TextInput(text=str(current_skill.name), id="skillname_{}"
                                        .format(str(id_number)), multiline=False)
                name_object.bind(on_text_validate=self.handle_skill_name)
            else:
                name_object = Label(text="{}".format(current_skill.name))
            self.label_text = str(current_skill.chance_to_increase)
            chance_label = Label(text="{}%".format(self.label_text),
                                 id="chance_{}".format(str(id_number)), size_hint_x=0.2)
            pass_button = Button(text="Pass", id="pass_{}".format(str(id_number)), size_hint_x=0.2)
            pass_button.bind(on_release=self.handle_pass_button)
            fail_button = Button(text="Fail", id="fail_{}".format(str(id_number)), size_hint_x=0.2)
            fail_button.bind(on_release=self.handle_fail_button)
            skill_level = TextInput(text=str(current_skill.level), id="level_{}"
                                    .format(str(id_number)), multiline=False)
            skill_level.bind(on_text_validate=self.handle_text)
            self.root.ids["box_{}".format(box)].add_widget(name_object)
            self.root.ids["box_{}".format(box)].add_widget(chance_label)
            self.root.ids["box_{}".format(box)].add_widget(skill_level)
            self.root.ids["box_{}".format(box)].add_widget(pass_button)
            self.root.ids["box_{}".format(box)].add_widget(fail_button)
        except AttributeError:
            return

    def handle_calculate(self):
        """Rolls dice to see if a skill levels up or not, if it does, resets the chance of levelling"""
        if self.current_player:
            for skill in self.current_player.skills:
                if skill.chance_to_increase > 0:
                    d100 = randint(1, 101)
                    if d100 + skill.chance_to_increase > 100:
                        skill.level += 1
                        skill.chance_to_increase = 0
            self.clear_widget(DEFAULT_TEXT)
            self.create_skills_widgets()
            self.current_player.save_player_skills(self.player_skills_to_filename[self.current_player.name])
        else:
            return

    def handle_text(self, instance):
        """Updates the player skill level to the inputted number"""
        id_number = instance.id.split("_")
        id_number = int(id_number[1])
        box = BOXES[id_number % 5]
        current_skill = self.current_player.skills[id_number]
        current_skill.level = int(instance.text)
        self.root.ids["box_{}".format(box)].clear_widgets()
        self.create_skills(box, id_number)
        self.current_player.save_player_skills(self.player_skills_to_filename[self.current_player.name])
        self.status_text = "{} Level Changed To {}".format(current_skill.name, instance.text)

    def handle_new_player(self):
        """Handle the New Player button event"""
        self.clear_widget(DEFAULT_TEXT)
        self.page_counter = 1
        self.update_title()
        name_label = Label(text="Player Name:")
        name_input = TextInput(multiline=False)
        instructions_label = Label(text="Press Enter When Done")
        name_input.bind(on_text_validate=self.new_player)
        exit_button = Button(text="Exit Player Creation")
        exit_button.bind(on_release=self.handle_exit_button)
        self.root.ids.box_2.add_widget(name_label)
        self.root.ids.box_3.add_widget(name_input)
        self.root.ids.box_4.add_widget(instructions_label)
        self.root.ids.box_5.add_widget(exit_button)

    def handle_exit_button(self, instance):
        if self.root.ids.content_selector.text == "Skills":
            self.clear_widget(DEFAULT_TEXT)
            self.create_skills_widgets()
        else:
            self.root.ids.content_selector.text = "Skills"

    def new_player(self, instance):
        """Adds a new player to the player list with default values"""
        name = instance.text.replace(".", "")
        if name in self.player_to_index:
            self.status_text = "{} Already Exists".format(name)
            return
        new_player = Player(name)
        new_player.load_player_skills("{}.csv".format(DEFAULT_FILE))
        new_player.load_player_attributes("{}_1.csv".format(DEFAULT_FILE))
        new_player.save_player_skills("{}.csv".format(name))
        new_player.save_player_attributes("{}_1.csv".format(name))
        self.clear_widget(DEFAULT_TEXT)
        self.get_spinner_values()
        self.status_text = "{} Added To The Player List".format(name)

    def get_spinner_values(self):
        """Gets any updates to the player list for the spinner options"""
        self.walk()
        self.root.ids.player_selector.values = self.player_to_index.keys()

    def handle_delete(self, name):
        """Deletes current player."""
        spinner = self.root.ids.player_selector
        self.page_counter = 1
        self.update_title()
        if not name == "":
            try:
                os.remove("{}.csv".format(name))
                os.remove("{}_1.csv".format(name))
                self.clear_widget(DEFAULT_TEXT)
                del (self.player_to_index[name])
                self.get_spinner_values()
                self.status_text = "{} Deleted!".format(spinner.text)
                spinner.text = ""
            except FileNotFoundError:
                self.status_text = "{} Doesn't Exist... They Were Already Deleted!!!".format(spinner.text)
        else:
            self.status_text = "Please Select A Player To Delete"
            return

    def content_swap(self, text):
        if self.current_player:
            self.clear_widget(DEFAULT_TEXT)
            self.page_counter = 1
            self.update_title()
            if text == "Skills":
                self.skill_index_start = 0
                self.create_skills_widgets()
            elif text == "Attributes":
                self.attribute_index_start = 0
                self.create_attributes_widgets()
        else:
            return

    def create_attributes_widgets(self):
        if self.current_player:
            for i, box in enumerate(BOXES, self.attribute_index_start):
                self.create_attributes(box, i)
        else:
            return

    def create_attributes(self, box, id_number):
        """Adds the labels, text input and buttons for the skills in the range"""
        try:
            current_attribute = self.current_player.attributes[id_number]
            if current_attribute.name == "SPARE":
                name_object = TextInput(text=str(current_attribute.name), id="attname_{}"
                                        .format(str(id_number)), multiline=False, size_hint_x=0.3)
                name_object.bind(on_text_validate=self.handle_attribute_name)
            else:
                name_object = Label(text="{}".format(current_attribute.name), size_hint_x=0.3)
            attribute_info = TextInput(text=str(current_attribute.quality), id="attribute_{}"
                                       .format(str(id_number)), multiline=False)
            attribute_info.bind(on_text_validate=self.handle_attribute_quality)
            self.root.ids["box_{}".format(box)].add_widget(name_object)
            self.root.ids["box_{}".format(box)].add_widget(attribute_info)
        except AttributeError:
            return

    def handle_attribute_quality(self, instance):
        id_number = instance.id.split("_")
        id_number = int(id_number[1])
        box = BOXES[id_number % 5]
        current_attribute = self.current_player.attributes[id_number]
        if current_attribute.name == "Notes":
            instance.text = instance.text.replace(",", "")
        current_attribute.quality = instance.text
        self.root.ids["box_{}".format(box)].clear_widgets()
        self.create_attributes(box, id_number)
        self.current_player.save_player_attributes(self.player_attributes_to_filename[self.current_player.name])
        self.status_text = "{} Properties Updates".format(current_attribute.name)

    def handle_attribute_name(self, instance):
        id_number = instance.id.split("_")
        id_number = int(id_number[1])
        box = BOXES[id_number % 5]
        current_attribute = self.current_player.attributes[id_number]
        current_attribute.name = instance.text
        self.root.ids["box_{}".format(box)].clear_widgets()
        self.create_attributes(box, id_number)
        self.current_player.save_player_attributes(self.player_attributes_to_filename[self.current_player.name])
        self.status_text = "SPARE Attribute Updated To {}".format(current_attribute.name)

    def handle_skill_name(self, instance):
        id_number = instance.id.split("_")
        id_number = int(id_number[1])
        box = BOXES[id_number % 5]
        current_skill = self.current_player.skills[id_number]
        current_skill.name = instance.text
        self.root.ids["box_{}".format(box)].clear_widgets()
        self.create_skills(box, id_number)
        self.current_player.save_player_skills(self.player_skills_to_filename[self.current_player.name])
        self.status_text = "SPARE Skill Updated To {}".format(current_skill.name)


if __name__ == '__main__':
    DndSkillTracker().run()
