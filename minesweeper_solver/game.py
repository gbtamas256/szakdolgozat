import numpy as np
import random as rn


def generate_key(n, m, k, index) -> np.ndarray:
    possible_coordinates = [(x, y) for x in range(n) for y in range(m)]
    possible_coordinates.remove(index)
    for nearby in take_nearby(n, m, *index):
        possible_coordinates.remove(nearby)
    coordinates = rn.sample(possible_coordinates, k)

    key = np.zeros((n, m), dtype=np.int8)
    for i in coordinates:
        if (0 < i[0] < n - 1) and (0 < i[1] < m - 1):
            key[i[0] - 1, i[1] - 1] += 1
            key[i[0] - 1, i[1]] += 1
            key[i[0] - 1, i[1] + 1] += 1
            key[i[0], i[1] - 1] += 1
            key[i[0], i[1] + 1] += 1
            key[i[0] + 1, i[1] - 1] += 1
            key[i[0] + 1, i[1]] += 1
            key[i[0] + 1, i[1] + 1] += 1
        elif i[0] == 0 and i[1] == 0:
            key[i[0], i[1] + 1] += 1
            key[i[0] + 1, i[1]] += 1
            key[i[0] + 1, i[1] + 1] += 1
        elif i[0] == 0 and i[1] == m - 1:
            key[i[0], i[1] - 1] += 1
            key[i[0] + 1, i[1] - 1] += 1
            key[i[0] + 1, i[1]] += 1
        elif i[0] == n - 1 and i[1] == 0:
            key[i[0] - 1, i[1]] += 1
            key[i[0] - 1, i[1] + 1] += 1
            key[i[0], i[1] + 1] += 1
        elif i[0] == n - 1 and i[1] == m - 1:
            key[i[0] - 1, i[1] - 1] += 1
            key[i[0] - 1, i[1]] += 1
            key[i[0], i[1] - 1] += 1
        elif i[0] == 0 and (0 < i[1] < m - 1):
            key[i[0], i[1] - 1] += 1
            key[i[0], i[1] + 1] += 1
            key[i[0] + 1, i[1] - 1] += 1
            key[i[0] + 1, i[1]] += 1
            key[i[0] + 1, i[1] + 1] += 1
        elif (0 < i[0] < n - 1) and i[1] == 0:
            key[i[0] - 1, i[1]] += 1
            key[i[0] - 1, i[1] + 1] += 1
            key[i[0], i[1] + 1] += 1
            key[i[0] + 1, i[1]] += 1
            key[i[0] + 1, i[1] + 1] += 1
        elif (0 < i[0] < n - 1) and i[1] == m - 1:
            key[i[0] - 1, i[1] - 1] += 1
            key[i[0] - 1, i[1]] += 1
            key[i[0], i[1] - 1] += 1
            key[i[0] + 1, i[1] - 1] += 1
            key[i[0] + 1, i[1]] += 1
        elif i[0] == n - 1 and (0 < i[1] < m - 1):
            key[i[0] - 1, i[1] - 1] += 1
            key[i[0] - 1, i[1]] += 1
            key[i[0] - 1, i[1] + 1] += 1
            key[i[0], i[1] - 1] += 1
            key[i[0], i[1] + 1] += 1

    for i in coordinates:
        key[i[0], i[1]] = 9
    return key


def generate_initial(n, m) -> np.ndarray:
    game = np.zeros((n, m), dtype=np.int8)
    return game


def take_nearby(n, m, i, j):
    """Returns a list of the adjacent tiles"""
    nearby = []
    if 0 < i < n - 1 and 0 < j < m - 1:
        nearby.append((i - 1, j - 1))
        nearby.append((i - 1, j))
        nearby.append((i - 1, j + 1))
        nearby.append((i, j - 1))
        nearby.append((i, j + 1))
        nearby.append((i + 1, j - 1))
        nearby.append((i + 1, j))
        nearby.append((i + 1, j + 1))
    elif i == 0 and 0 < j < m - 1:
        nearby.append((i, j - 1))
        nearby.append((i, j + 1))
        nearby.append((i + 1, j - 1))
        nearby.append((i + 1, j))
        nearby.append((i + 1, j + 1))
    elif 0 < i < n - 1 and j == 0:
        nearby.append((i - 1, j))
        nearby.append((i - 1, j + 1))
        nearby.append((i, j + 1))
        nearby.append((i + 1, j))
        nearby.append((i + 1, j + 1))
    elif 0 < i < n - 1 and j == m - 1:
        nearby.append((i - 1, j - 1))
        nearby.append((i - 1, j))
        nearby.append((i, j - 1))
        nearby.append((i + 1, j - 1))
        nearby.append((i + 1, j))
    elif i == n - 1 and 0 < j < m - 1:
        nearby.append((i - 1, j - 1))
        nearby.append((i - 1, j))
        nearby.append((i - 1, j + 1))
        nearby.append((i, j - 1))
        nearby.append((i, j + 1))
    elif i == 0 and j == 0:
        nearby.append((i, j + 1))
        nearby.append((i + 1, j))
        nearby.append((i + 1, j + 1))
    elif i == 0 and j == m - 1:
        nearby.append((i, j - 1))
        nearby.append((i + 1, j - 1))
        nearby.append((i + 1, j))
    elif i == n - 1 and j == 0:
        nearby.append((i - 1, j))
        nearby.append((i - 1, j + 1))
        nearby.append((i, j + 1))
    elif i == n - 1 and j == m - 1:
        nearby.append((i - 1, j - 1))
        nearby.append((i - 1, j))
        nearby.append((i, j - 1))
    return nearby


def reveal_nearby(state, key, i, j):
    """Reveals the adjacent unknown tiles, recursively in case of a 0 key"""
    n, m = state.shape
    nearby = []
    for u in take_nearby(n, m, i, j):
        if state[u] == 0:
            nearby.append(u)
            state[u] = 1
            if key[u] == 0:
                reveal_nearby(state, key, *u)
