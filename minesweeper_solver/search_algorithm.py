import numpy as np
import game
import random


def my_search(minesweeper, state: np.matrix, key: np.matrix) -> tuple[bool, list]:  # Return is_flag, step;  state: status of the tiles, key: number of nearby bombs
    # IN STATE  0: unknown, 1: empty, 2: flag, 3: bomb
    is_flag: bool = False
    n, m = state.shape
    fifty_fifties = []
    one_in_threes = []
    for i in range(n):
        for j in range(m):
            if state[i][j] == 1:
                if key[i][j] == 0:
                    continue
                u_counter = 0
                f_counter = 0
                unknowns = []
                for nearby in game.take_nearby(n, m, i, j):
                    if state[nearby] == 0:
                        u_counter += 1
                        unknowns.append(nearby)
                    if state[nearby] == 2:
                        f_counter += 1
                if f_counter != key[i][j]:
                    if u_counter + f_counter == key[i][j]:
                        """Flags the known position of bombs"""
                        is_flag = True
                        return is_flag, unknowns
                    if u_counter > key[i][j] - f_counter:
                        if u_counter / (key[i][j] - f_counter) == 2:
                            fifty_fifties.append(unknowns)
                        if u_counter / (key[i][j] - f_counter) == 3:
                            one_in_threes.append(unknowns)
                elif u_counter != 0:
                    """Reveals the tile that is not a bomb"""
                    return is_flag, unknowns

    for i in range(n):
        for j in range(m):
            if state[i][j] == 1:
                if key[i][j] == 0:
                    continue
                u_counter = 0
                f_counter = 0
                unknowns = []
                for nearby in game.take_nearby(n, m, i, j):
                    if state[nearby] == 0:
                        u_counter += 1
                        unknowns.append(nearby)
                    if state[nearby] == 2:
                        f_counter += 1
                if f_counter != key[i][j]:
                    for u in range(n):
                        for v in range(m):
                            if state[u][v] == 1:
                                if abs(u - i) < 3 and abs(v - j) < 3 and (u, v) != (i, j):
                                    """Takes logical steps and returns if there is a conclusion"""
                                    shared = shared_unknowns(state, i, j, u, v)
                                    output = evaluate_shared(state, key, shared, i, j, u, v)
                                    if output is not None:
                                        return output

    if fifty_fifties:
        return is_flag, fifty_fifties[0][0]
    elif one_in_threes:
        return is_flag, one_in_threes[0][0]
    else:
        return is_flag, random.choice(minesweeper.legal_steps(state))


def evaluate_shared(state, key, shared, i, j, u, v) -> tuple[bool, list] | None:
    """Decides if I can do anything with the shared unknowns"""
    real_value_1 = key[i, j] - count_flags(state, i, j)
    real_value_2 = key[u, v] - count_flags(state, u, v)
    nearby_unknowns_1 = take_nearby_unknowns(state, i, j)
    nearby_unknowns_2 = take_nearby_unknowns(state, u, v)
    if real_value_1 - (len(nearby_unknowns_1) - len(shared)) == real_value_2:
        for item in shared:
            nearby_unknowns_2.remove(item)
        if nearby_unknowns_2:
            return False, nearby_unknowns_2
    elif real_value_2 - real_value_1 == len(nearby_unknowns_2) - len(shared):
        for item in shared:
            nearby_unknowns_2.remove(item)
        if nearby_unknowns_2:
            return True, nearby_unknowns_2
    else:
        return None


def count_flags(state, i, j):
    n, m = state.shape
    counter = 0
    for nearby in game.take_nearby(n, m, i, j):
        if state[nearby] == 2:
            counter += 1
    return counter


def take_nearby_unknowns(state, i, j):
    """Returns the list of adjacent tiles that are unknown"""
    n, m = state.shape
    nearby = []
    for u in game.take_nearby(n, m, i, j):
        if state[u] == 0:
            nearby.append(u)
    return nearby


def shared_unknowns(state, i, j, u, v):
    """Returns the shared unknown tiles of two indexes"""
    near_1 = set(take_nearby_unknowns(state, i, j))
    near_2 = set(take_nearby_unknowns(state, u, v))
    shared = list(near_1.intersection(near_2))
    return shared
