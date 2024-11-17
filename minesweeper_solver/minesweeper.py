import random
import game
import numpy as np
from search_algorithm import my_search


class Minesweeper:

    def __init__(self, starting_pos, n, m, k):
        self.n = n
        self.m = m
        self.k = k

        self.starting_pos = starting_pos

        self.key: np.ndarray = game.generate_key(self.n, self.m, self.k, self.starting_pos)  # 9: bomb, any other number: number of bombs nearby
        self.initial: np.ndarray = game.generate_initial(self.n, self.m)                     # STATE:  0: unknown, 1: empty, 2: flag, 3: bomb

    def legal_steps(self, state):
        """List of possible steps"""
        acts = []
        for i in range(self.n):
            for j in range(self.m):
                if state[i, j] == 0:
                    acts.append((i, j))
        return acts

    def take_step(self, steps, state, is_flag):
        """What happens when the chosen step is taken"""
        new_state = state
        if type(steps) is list:
            for step in steps:
                i, j = step
                if is_flag:
                    new_state[i, j] = 2
                elif self.key[i, j] != 9:
                    if self.key[i, j] == 0:
                        game.reveal_nearby(new_state, self.key, i, j)
                    new_state[i, j] = 1
        else:
            i, j = steps
            if is_flag:
                new_state[i, j] = 2
            elif self.key[i, j] != 9:
                if self.key[i, j] == 0:
                    game.reveal_nearby(new_state, self.key, i, j)
                new_state[i, j] = 1
            else:
                new_state[i, j] = 3

        return new_state

    def is_leaf(self, state):
        """Checks if the game is over either way"""
        counter = 0
        for i in range(self.n):
            for j in range(self.m):
                if state[i, j] == 0 or state[i][j] == 2:
                    counter += 1
                elif state[i, j] == 3:
                    return -1
        if counter > self.k:
            return 0
        else:
            return 1

    def goodness(self, state):
        if self.is_leaf(state) == 1:
            return "VICTORY"
        elif self.is_leaf(state) == -1:
            return "DEFEAT"

    def print(self, state):
        """Prints out the current state."""
        for i in range(self.n):
            for j in range(self.m):
                print(' ', end='')
                if state[i, j] == 1:
                    print(self.key[i, j], end=' ')
                elif state[i, j] == 2:
                    print('F', end=' ')
                elif state[i, j] == 0:
                    print('□', end=' ')
            print()
        print()

    def last_print(self, state):  # SYMBOLS:    □: unknown, ◆: stepped on bomb, ◇: unknown bomb, F: flag
        """Last printout for when the game is over"""
        if self.is_leaf(state) == -1:  # LOSS
            for i in range(self.n):
                for j in range(self.m):
                    print(' ', end='')
                    if state[i, j] == 1:
                        print(self.key[i, j], end=' ')
                    elif state[i, j] == 0:
                        if self.key[i, j] == 9:
                            print('◇', end=' ')
                        else:
                            print('□', end=' ')
                    elif state[i, j] == 2:
                        print('F', end=' ')
                    else:
                        print('◆', end=' ')
                print()
            print()
        elif self.is_leaf(state) == 1:  # VICTORY
            for i in range(self.n):
                for j in range(self.m):
                    print(' ', end='')
                    if state[i, j] == 1:
                        print(self.key[i, j], end=' ')
                    elif state[i, j] == 2 or state[i, j] == 0:
                        print('F', end=' ')
                print()
            print()


# PLAYERS
def random_player(game, state, key):
    """Randomly choose between options"""
    return False, random.choice(game.legal_steps(state))


def my_player(game, state, key):
    return my_search(game, state, key)


def play_game(game: Minesweeper, player):  # Returns a list of all the states, the key and the ending
    state = game.initial
    print(f'Starting step: ({game.starting_pos[0]}, {game.starting_pos[1]}), flag: {False}')
    state: np.array = game.take_step(game.starting_pos, state, False)
    states: list = [state.tolist()]
    while True:
        game.print(state)
        is_flag, step = player(game, state, game.key)
        print(f'Current step(s): {", ".join(f"{i}" for i in step)}, flag: {is_flag}')
        state = game.take_step(step, state, is_flag)
        states.append(state.tolist())
        if game.is_leaf(state):
            game.last_print(state)
            ending = game.goodness(state)
            print(ending)
            return states, game.key, ending
