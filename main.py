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

DEFAULT_FILE = "DEFAULT_PLAYER.csv"
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
        self.player_to_filename = {}
        self.players = []
        self.index_start = 0
        self.player_number = 0

    def build(self):
        """Build the Kivy app from the .kv file"""
        self.status_text = "Press 'Enter' In Text Box To Apply New Levels"
        self.update_title()
        self.root = Builder.load_file('gui.kv')
        os.chdir('Players')
        self.walk()
        self.root.ids.player_selector.values = self.player_to_index.keys()
        return self.root

    def handle_next(self):
        """Displays the next set of skill widgets"""
        if self.page_counter == 10:
            return
        if self.current_player:
            self.clear_widget()
            self.page_counter += 1
            self.update_title()
            self.index_start += 5
            for i, box in enumerate(BOXES, self.index_start):
                self.create_widget(box, i)
        else:
            return

    def handle_previous(self):
        """Displays the previous set of skill widgets"""
        if self.page_counter == 1:
            return
        self.page_counter -= 1
        self.update_title()
        self.clear_widget()
        self.index_start -= 5
        for i, box in enumerate(BOXES, self.index_start):
            self.create_widget(box, i)

    def character_swap(self, player):
        """Changes the current character and resets all things accordingly"""
        self.page_counter = 1
        self.update_title()
        try:
            player_index = self.player_to_index[player]
            self.current_player = self.players[player_index]
            self.index_start = 0
            self.clear_widget()
            for i, box in enumerate(BOXES, self.index_start):
                self.create_widget(box, i)
        except KeyError:
            return

    def update_title(self):
        """Updates the title of the app"""
        self.title = "Dungeons and Dragons Skill Tracker Page {}".format(self.page_counter)

    def walk(self):
        """Process all subdirectories using os.walk()."""
        for directory_name, subdirectories, file_names in os.walk('.'):
            for file in file_names:
                if file == DEFAULT_FILE:
                    continue
                self.add_player(file)

    def add_player(self, file):
        """Adds player to the player list from the file"""
        player_name = self.get_player_name(file)
        if player_name in self.player_to_index:
            return
        player = Player(player_name)
        player.load_player(file)
        self.players.append(player)
        self.player_to_filename[player_name] = file
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
        return player

    def clear_widget(self):
        """Deletes all the dynamic widgets"""
        for box in BOXES:
            self.root.ids["box_{}".format(box)].clear_widgets()
        self.status_text = "Press 'Enter' In Text Box To Apply New Levels"

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
        self.create_widget(box, id_number)
        self.status_text = "{} Roll Succeeded. 10% Added to Level Up Chance".format(current_skill.name)

    def handle_fail_button(self, instance):
        """Adds 5% to level chance on failed skill use"""
        id_number = instance.id.split("_")
        id_number = int(id_number[1])
        box = BOXES[id_number % 5]
        current_skill = self.current_player.skills[id_number]
        if current_skill.chance_to_increase < 100:
            current_skill.chance_to_increase += 5
        self.root.ids["box_{}".format(box)].clear_widgets()
        self.create_widget(box, id_number)
        self.status_text = "{} Roll Failed. 5% Added to Level Up Chance".format(current_skill.name)

    def create_widget(self, box, id_number):
        """Adds the labels, text input and buttons for the skills in the range"""
        current_skill = self.current_player.skills[id_number]
        self.label_text = str(current_skill.chance_to_increase)
        chance_label = Label(text="{}%".format(self.label_text),
                             id="chance_{}".format(str(id_number)), size_hint_x=0.2)
        pass_button = Button(text="Pass", id="pass_{}".format(str(id_number)), size_hint_x=0.2)
        pass_button.bind(on_release=self.handle_pass_button)
        fail_button = Button(text="Fail", id="fail_{}".format(str(id_number)), size_hint_x=0.2)
        fail_button.bind(on_release=self.handle_fail_button)
        skill_label = Label(text=current_skill.name)
        skill_level = TextInput(text=str(current_skill.level), id="level_{}"
                                .format(str(id_number)), multiline=False)
        skill_level.bind(on_text_validate=self.handle_text)
        self.root.ids["box_{}".format(box)].add_widget(skill_label)
        self.root.ids["box_{}".format(box)].add_widget(chance_label)
        self.root.ids["box_{}".format(box)].add_widget(skill_level)
        self.root.ids["box_{}".format(box)].add_widget(pass_button)
        self.root.ids["box_{}".format(box)].add_widget(fail_button)

    def handle_calculate(self):
        """Rolls dice to see if a skill levels up or not, if it does, resets the chance of levelling"""
        if self.current_player:
            for skill in self.current_player.skills:
                if skill.chance_to_increase > 0:
                    d100 = randint(1, 101)
                    if d100 + skill.chance_to_increase > 100:
                        skill.level += 1
                        skill.chance_to_increase = 0
            self.clear_widget()
            for i, box in enumerate(BOXES, self.index_start):
                self.create_widget(box, i)
            self.current_player.save_player(self.player_to_filename[self.current_player.name])
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
        self.create_widget(box, id_number)
        self.current_player.save_player(self.player_to_filename[self.current_player.name])
        self.status_text = "{} Level Changed To {}".format(current_skill.name, instance.text)

    def handle_new_player(self):
        """Handle the New Player button event"""
        self.clear_widget()
        self.page_counter = 1
        self.update_title()
        name_label = Label(text="Player Name:")
        name_input = TextInput(multiline=False)
        instructions_label = Label(text="Press Enter When Done")
        name_input.bind(on_text_validate=self.new_player)
        self.root.ids.box_2.add_widget(name_label)
        self.root.ids.box_3.add_widget(name_input)
        self.root.ids.box_4.add_widget(instructions_label)

    def new_player(self, instance):
        """Adds a new player to the player list with default values"""
        instance.text = instance.text.replace(".", "")
        new_player = Player(instance.text)
        new_player.load_player(DEFAULT_FILE)
        new_player.save_player("{}.csv".format(instance.text))
        self.clear_widget()
        self.get_spinner_values()
        self.status_text = "{} Added To The Player List".format(instance.text)

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
                self.clear_widget()
                del (self.player_to_index[name])
                self.get_spinner_values()
                self.status_text = "{} Deleted!".format(spinner.text)
                spinner.text = ""
            except FileNotFoundError:
                self.status_text = "{} Doesn't Exist... They Were Already Deleted!!!".format(spinner.text)
        else:
            self.status_text = "Please Select A Player To Delete First"
            return


if __name__ == '__main__':
    DndSkillTracker().run()
