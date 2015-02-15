__author__ = 'davide'

import sys
import random
import itertools as it
import operator
from functools import lru_cache
from collections import Counter


def start(N):
    def get_menaces(sol, row, col):
        return sum(attacks((r, c), (row, col))
            for c, r in enumerate(sol, start=1))

    r = []
    pool = set()
    n = 1
    while n < N:
        els = [(i, get_menaces(r, i, n)) for i in range(1, N + 1)]
        min_val = min(els, key=operator.itemgetter(1))[1]
        min_vals = {el[0] for el in els if el[1] == min_val}
        min_vals.difference_update(pool)
        if min_vals:
            c = random.sample(min_vals, 1)[0]
        else:
            els = set(range(1, N + 1)) - pool
            c = random.sample(els, 1)[0]
        r.append(c)
        pool.add(c)
        n += 1

    el = (set(range(1, N + 1)) - pool).pop()
    r.append(el)
    return r


@lru_cache()
def attacks(pos_1, pos_2):
    return (pos_1[0] == pos_2[0] or
            pos_1[1] == pos_2[1] or
            abs(pos_1[0] - pos_2[0]) == abs(pos_1[1] - pos_2[1]))


def print_board(positions):
    for i in range(N):
        print("|", end="")
        for j in range(N):
            if positions[j] == i + 1:
                print("O", end="")
            else:
                print(" ", end="")
            print("|", end="")
        print()


def find_conflict_var(sol, N, last):
    def is_in_conflict(v):
        r = sol[v - 1]
        return any(v != c1 and attacks((r, v), (r1, c1))
            for c1, r1 in enumerate(sol, start=1))

    pool = list(range(1, N + 1))
    if last is not None:
        pool.remove(last)
    while pool:
        v = random.choice(pool)
        if is_in_conflict(v):
            return v
        pool.remove(v)
    if last and is_in_conflict(last):
        return last


def set_value(sol, var, value):
    index = sol.index(value)
    sol[var - 1], sol[index] = value, sol[var - 1]


def num_of_conflicts(sol, var):
    row = sol[var - 1]
    return sum(var != c1 and attacks((row, var), (r1, c1))
        for c1, r1 in enumerate(sol, start=1))


def select_value(var, current, N):
    conflicts_vec = []
    current_o = current[:]
    for val in range(1, N + 1):
        set_value(current_o, var, val)
        conflicts_vec.append(num_of_conflicts(current_o, var))
        current_o = current[:]
    min_c = min(conflicts_vec)
    return random.choice([i for (i, v) in enumerate(conflicts_vec, start=1)
                          if v == min_c])


def min_conflicts(N, callback, c2, max_passi=100000):
    current = start(N)

    nc = sum(num_of_conflicts(current, i) for i in range(1, N + 1))
    c2(current, nc)

    last = None
    for it in range(max_passi):
        var = find_conflict_var(current, N, last)
        last = var
        if var is None:
            callback(None, None, current)
            return current, it
        val = select_value(var, current, N)
        callback(var, val, current)
        set_value(current, var, val)
    return None, max_passi