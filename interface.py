"""
This file is part of Briscola.

Briscola is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Briscola is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Briscola. If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np
import npyscreen
from deck import *
from better_card import *

player_file = input("Type the name of the file where the enemy AI is saved. ")
opponent = np.load(player_file)

#Since we save the players as an array, the user might
#try to input the entire array instead of a single player.
try:
    if len(opponent) > 1:
        opponent = opponent[0]

except TypeError:
    pass

briscola = ["B", "D", "C", "S"][np.random.randint(0, 4)]
full_name = {"B": "Bastoni", "D": "Denari", "C": "Coppa", "S": "Spade"}

class human_player():
    def _init_(self):
        self.points = 0
        self.hand = []
        self.best = False

class App(npyscreen.StandardApp):
    def startup(self):
        self.addForm("MAIN", MainForm, name = "Briscola")

class OpponentScreen(npyscreen.BoxTitle)
