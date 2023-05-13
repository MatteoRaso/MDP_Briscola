"""
This file is part of Briscola.

Briscola is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Briscola is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Briscola. If not, see <https://www.gnu.org/licenses/>. 
"""

#!/usr/bin/python
#When two players play their card, this function is called to determine who wins.
#player_1 is the one that plays first.
#The reason that we have a 'best' attribute is because whoever has the best card
#gets to draw and play first for the next card.
def better_card(card_1, card_2, player_1, player_2, briscola):

    total_points = card_1.points + card_2.points

    player_1.best = False
    player_2.best = False

    if card_1.suit == card_2.suit:
        if card_1.points > card_2.points:
            player_1.points += total_points
            player_1.best = True

        elif card_1.index > card_2.index:
            player_1.points += total_points
            player_1.best = True

        else:
            player_2.points += total_points
            player_2.best = True

    elif card_2.suit == briscola:
        player_2.points += total_points
        player_2.best = True

    else:
        player_1.points += total_points
        player_1.best = True

    return player_1, player_2
