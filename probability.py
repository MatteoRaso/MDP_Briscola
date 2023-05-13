"""
This file is part of Briscola.

Briscola is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Briscola is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Briscola. If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np
from deck import *

#For this markov decision process, I'll need P_a(s, s').
#Normally, this function is approximated with a generative model,
#but I can estimate the probability by analysing a very large amount of hands.
#We'll use a 3D array to show every probability.
#The first axis will have a size of 4 to represent the 4
#different actions that we can take. This comes to
#4 different transition matrices.
#State i is when the point difference is
#i + 120, where -120 < i < 120.


#It doesn't matter what suit we use here.
new_deck = deck("B")
num_of_simulations = 70000000

probability_array = np.zeros((4, 241, 241))
times_action_was_chosen = np.zeros(4)

for i in range(0, num_of_simulations):
    point_difference = np.random.randint(-120, 121)

    initial_state = point_difference + 120

    hands = np.random.choice(new_deck, 6, False)
    hand_1 = list(hands[0:3])
    hand_2 = list(hands[3:6])

    #If we only have briscolas, then we can't use action 2 or 3.
    if hand_1[0].suit == "B" and hand_1[1].suit == "B" and hand_1[2].suit == "B":
        possible_actions = [0, 1]

    #Action 0 is to play the better briscola and action 1 is to play the worst one.
    #We have to make sure that the hand has 2 briscolas for the actions to be possible.
    #However, we can't do action 3, which is to pick the worst non-briscola hand.
    elif (hand_1[0].suit == "B" and hand_1[1].suit == "B") or (hand_1[0].suit == "B" and hand_1[2].suit == "B") or (hand_1[1].suit == "B" and hand_1[2].suit == "B"):
        possible_actions = [0, 1, 2]

    #If we only have 1 briscola, we can still do action 0, since the only
    #briscola is also the best briscola by default.
    elif (hand_1[0].suit == "B") or (hand_1[1].suit == "B") or (hand_1[2].suit == "B"):
        possible_actions = [0, 2, 3]

    #No briscolas.
    else:
        possible_actions = [2, 3]

    choice = np.random.randint(0, len(possible_actions))
    action = possible_actions[choice]
    times_action_was_chosen[action] += 1

    if action == 0:
        possible_hands = []
        for card in hand_1:
            if card.suit == "B":
                possible_hands.append(card)

        possible_hands.sort(key = lambda x: x.points, reverse = True)
        played_card = possible_hands[0]

    elif action == 1:
        possible_hands = []
        for card in hand_1:
            if card.suit == "B":
                possible_hands.append(card)

        possible_hands.sort(key = lambda x: x.points, reverse = True)
        played_card = possible_hands[1]

    elif action == 2:
        possible_hands = []
        for card in hand_1:
            if card.suit != "B":
                possible_hands.append(card)

        possible_hands.sort(key = lambda x: x.points, reverse = True)
        played_card = possible_hands[0]

    else:
        possible_hands = []
        for card in hand_1:
            if card.suit != "B":
                possible_hands.append(card)

        possible_hands.sort(key = lambda x: x.points, reverse = True)
        played_card = possible_hands[1]

    #When you play cards, it's generally a good idea to assume
    #that your opponent is better than you. Because of that,
    #I'm going to calculate the probability as if the
    #opponent can see the player's cards.
    hand_2.sort(key = lambda x: x.points, reverse = True)
    if action == 0 or action == 1:
        if hand_2[0] != "B" and hand_2[1] != "B" and hand_2[2] != "B":
            #Play the weakest card to deprive the player of points
            point_difference += hand_2[-1].points

        else:
            possible_hands = []
            for card in hand_2:
                if card.suit == "B":
                    possible_hands.append(card)

            possible_hands.sort(key = lambda x: x.points, reverse = True)
            #Play the best hand to gain the immediate advantage
            if played_card.points < possible_hands[0].points:
                point_difference -= possible_hands[0].points

            else:
                point_difference += possible_hands[-1].points

    elif played_card.points < possible_hands[0].points:
        point_difference -= possible_hands[0].points

    else:
        point_difference += possible_hands[-1].points

    #The absolute point difference can't be greater than 120
    #because there are only 120 points in the game.
    if point_difference <= -120:
        new_state = 0

    elif point_difference >= 120:
        new_state = 240

    else:
        new_state = point_difference + 120

    probability_array[action][initial_state][new_state] += 1

    #Just so we know the program is running
    if i % 1000 == 0:
        print(i)

#The distribution should be roughly 19.8% for action 0,
#5.19% for action 1, 39.7% for action 2 and
#35.2% for action 3.
print(times_action_was_chosen)
#Normalizes the results so that the sum of each row is 1
for i in range(0, 4):
    probability_array[i] = (probability_array[i].T / np.sum(probability_array[i], 1).T).T
    for j in range(0, len(probability_array[i])):
        assert abs(sum(probability_array[i][j]) - 1) < 1e-3

np.save("probability.npy", probability_array)
