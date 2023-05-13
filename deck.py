"""
This file is part of Briscola.

Briscola is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Briscola is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Briscola. If not, see <https://www.gnu.org/licenses/>.
"""
#!/usr/bin/python

from card import *
import csv

def deck(briscola):
    new_deck = []
    with open("every_card.csv", mode ='r') as file:
        csv_file = csv.reader(file)

        for lines in csv_file:
            new_card = card()
            new_card.suit = lines[0]
            new_card.value = lines[1]
            new_card.points = int(lines[2])
            new_card.index = int(lines[3])
            new_card.set_briscola(briscola)

            new_deck.append(new_card)

    return new_deck

