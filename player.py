"""
This file is part of Briscola.

Briscola is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Briscola is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Briscola. If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np

class player():
    def _init_(self):
        self.points = 0
        self.wins = 0
        self.hand = []
        #If they have the better hand
        self.best = False
        self.probability = np.load("probability.npy")
        #There'll be times where certain actions
        #will be impossible, so we need several
        #values and policies for each situation.
        self.value_1 = {0: 0}
        self.policy_1 = {0: 0}
        self.value_2 = {0: 0}
        self.policy_2 = {0: 0}
        self.value_3 = {0: 0}
        self.policy_3 = {0: 0}
        self.value_4 = {0: 0}
        self.policy_4 = {0: 0}
        self.training_iterations = 0
        self.gamma = 0

    def reward(self, state_i, state_j):
        y = state_j - state_i
        return y

    def initialize_policy_and_value(self):
        for i in range(1, 241):
            self.policy_1[i] = 0
            self.value_1[i] = 0
            self.policy_2[i] = 0
            self.value_2[i] = 0
            self.policy_3[i] = 0
            self.value_3[i] = 0
            self.policy_4[i] = 0
            self.value_4[i] = 0

    def policy_1_update(self, state):
        policy_guess = -1
        best_score = -1e30
        best_answer = -1
        for action in [0, 1]:
            score = 0
            #Since you can only score 22 points in a single hand,
            #We can look at the 22 states in either direction
            #and ignore all the 0 elements in the transition matrix.
            #I'm putting 23 here instead of 22 just so we don't
            #accidently leave behind an element, since range(i, j)
            #is [i, j).
            for new_state in range(max(0, state - 23), min(241, state + 23)):
                score += self.probability[action][state][new_state] * (self.reward(state, new_state) * self.gamma * self.value_1[new_state])

            if score > best_score:
                best_score = score
                best_answer = action

        self.policy_1[state] = best_answer

    def policy_2_update(self, state):
        policy_guess = -1
        best_score = -1e30
        best_answer = -1
        for action in [0, 1, 2]:
            score = 0
            for new_state in range(max(0, state - 23), min(241, state + 23)):
                score += self.probability[action][state][new_state] * (self.reward(state, new_state) * self.gamma * self.value_2[new_state])

            if score > best_score:
                best_score = score
                best_answer = action

        self.policy_2[state] = best_answer

    def policy_3_update(self, state):
        policy_guess = -1
        best_score = -1e30
        best_answer = -1
        for action in [0, 2, 3]:
            score = 0
            for new_state in range(max(0, state - 23), min(241, state + 23)):
                score += self.probability[action][state][new_state] * (self.reward(state, new_state) * self.gamma * self.value_3[new_state])

            if score > best_score:
                best_score = score
                best_answer = action

        self.policy_3[state] = best_answer

    def policy_4_update(self, state):
        policy_guess = -1
        best_score = -1e30
        best_answer = -1
        for action in [2, 3]:
            score = 0
            for new_state in range(max(0, state - 23), min(241, state + 23)):
                score += self.probability[action][state][new_state] * (self.reward(state, new_state) * self.gamma * self.value_4[new_state])

            if score > best_score:
                best_score = score
                best_answer = action

        self.policy_4[state] = best_answer

    def value_1_update(self, state):
        action = self.policy_1[state]
        new_value = 0
        for new_state in range(max(0, state - 23), min(241, state + 23)):
            new_value += self.probability[action][state][new_state] * (self.reward(state, new_state) * self.gamma * self.value_1[new_state])

        self.value_1[state] = new_value

    def value_2_update(self, state):
        action = self.policy_2[state]
        new_value = 0
        for new_state in range(max(0, state - 23), min(241, state + 23)):
            new_value += self.probability[action][state][new_state] * (self.reward(state, new_state) * self.gamma * self.value_2[new_state])

        self.value_2[state] = new_value

    def value_3_update(self, state):
        action = self.policy_3[state]
        new_value = 0
        for new_state in range(max(0, state - 23), min(241, state + 23)):
            new_value += self.probability[action][state][new_state] * (self.reward(state, new_state) * self.gamma * self.value_3[new_state])

        self.value_3[state] = new_value

    def value_4_update(self, state):
        action = self.policy_4[state]
        new_value = 0
        for new_state in range(max(0, state - 23), min(241, state + 23)):
            new_value += self.probability[action][state][new_state] * (self.reward(state, new_state) * self.gamma * self.value_4[new_state])

        self.value_4[state] = new_value

    def train(self):
        for i in range(0, self.training_iterations):
            state = np.random.randint(0, 241)
            self.value_1_update(state)
            self.policy_1_update(state)
            self.value_2_update(state)
            self.policy_2_update(state)
            self.value_3_update(state)
            self.policy_3_update(state)
            self.value_4_update(state)
            self.policy_4_update(state)

            #Let's us know something is happening.
            if i % 1000 == 0:
                print(i)

    def play_card(self, opponent, briscola):
        state = int(120 + self.points - opponent.points)
        try:
            if self.hand[0].suit == briscola and self.hand[1].suit == briscola and self.hand[2].suit == briscola:
                action = self.policy_1[state]
                print(action)

            elif ((self.hand[0].suit == briscola and self.hand[1].suit == briscola)
            or (self.hand[0].suit == briscola and self.hand[2].suit == briscola)
            or (self.hand[1].suit == briscola and self.hand[2].suit == briscola)):
                action = self.policy_2[state]

            elif (self.hand[0].suit == briscola) or (self.hand[1].suit == briscola) or (self.hand[2].suit == briscola):
                action = self.policy_3[state]

            else:
                action = self.policy_4[state]

        except IndexError:
            action = 0

        if action == 0:
            possible_hands = []
            for card in self.hand:
                if card.suit == briscola:
                    possible_hands.append(card)

            possible_hands.sort(key = lambda x: x.points, reverse = True)
            played_card = possible_hands[0]

        elif action == 1:
            possible_hands = []
            for card in self.hand:
                if card.suit == briscola:
                    possible_hands.append(card)

            possible_hands.sort(key = lambda x: x.points, reverse = True)
            played_card = possible_hands[-1]

        elif action == 2:
            possible_hands = []
            for card in self.hand:
                if card.suit != briscola:
                    possible_hands.append(card)

            possible_hands.sort(key = lambda x: x.points, reverse = True)
            played_card = possible_hands[0]

        else:
            possible_hands = []
            for card in self.hand:
                if card.suit != briscola:
                    possible_hands.append(card)

            possible_hands.sort(key = lambda x: x.points, reverse = True)
            played_card = possible_hands[-1]

        return played_card
