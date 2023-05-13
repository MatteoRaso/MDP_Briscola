"""
This file is part of Briscola.

Briscola is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Briscola is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Briscola. If not, see <https://www.gnu.org/licenses/>.
"""
#!/usr/bin/python

class card():
    def _init_(self):
        self.suit = ''
        self.is_briscola = False
        #A bit useless since we have the points attribute,
        #but we'll need to know the card value if we want to make a GUI.
        self.value = 0
        self.points = 0
        #Too long to explain this one here - see commit message
        self.index = -1

    def set_briscola(self, briscola):
        if self.suit == briscola:
            self.is_briscola = True
