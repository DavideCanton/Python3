# cython: language_level=3

__author__ = 'davide'

import sys
import random
import itertools as it
import operator
from collections import Counter
cimport numpy as np
import numpy as np

ctypedef np.int32_t np_type
DTYPE = np.int32
cdef int N = 20

cdef int get_menaces(np.ndarray[np_type, ndim=1] sol, int row, int col):
    cdef int r, c, s = 0
    for c in range(1, N + 1):
        r = sol[c - 1]
        s += <bint> attacks(r, c, row, col)
    return s

cdef object start(int factor):
    cdef np.ndarray[np_type, ndim=1] assignment = np.zeros(N, dtype=DTYPE)
    pool = set()
    whole = set(range(1, N + 1))
    cdef int n = 1
    cdef int last = 0

    while n < N:
        els = [(col, get_menaces(assignment, col, n))
               for col in range(1, N + 1)]
        min_val = min(els, key=operator.itemgetter(1))[1]
        min_rows = {el[0] for el in els if el[1] == min_val}
        min_rows.difference_update(pool)
        if min_rows:
            element = random.sample(min_rows, 1)[0]
        else:
            els = whole - pool
            element = random.sample(els, 1)[0]
        assignment[last] = element
        last += 1
        pool.add(element)
        n += 1

    last_element = (whole - pool).pop()
    assignment[last] = last_element
    if factor > 0:
        n = 0
        for i in range(1, N + 1):
            n += num_of_conflicts(assignment, i)
        print("Starting from", assignment, "\n#conflicts =", n)
    return assignment


cdef int attacks(int x1, int y1, int x2, int y2):
    return x1 == x2 or y1 == y2 or abs(x1-x2) == abs(y1-y2)


def print_board(positions):
    for i in range(len(positions)):
        print("|", end="")
        for j in range(len(positions)):
            if positions[j] == i + 1:
                print("O", end="")
            else:
                print(" ", end="")
            print("|", end="")
        print()


cdef int is_in_conflict(np.ndarray[np_type, ndim=1] sol, int v):
    cdef int r = sol[v - 1]
    cdef int r1, c1
    for c1 in range(1, N+1):
        if c1 != v:
            r1 = sol[c1 - 1]
            if attacks(r, v, r1, c1):
                return True
    return False

cdef int find_conflict_var(sol, int last):
    cdef int v
    pool = list(range(1, N + 1))
    if last > 0:
        pool.remove(last)
    while pool:
        v = random.choice(pool)
        if is_in_conflict(sol, v):
            return v
        pool.remove(v)
    if last > 0 and is_in_conflict(sol, last):
        return last
    return -1


cdef int set_value(np.ndarray[np_type, ndim=1] sol, int var, int value) except 0:
    cdef int index = -1, i
    for i in range(N):
        if sol[i] == value:
            index = i
            break
    sol[index] = sol[var - 1]
    sol[var - 1] = value
    return 1


cdef int num_of_conflicts(np.ndarray[np_type, ndim=1] sol, int var):
    cdef int row = sol[var - 1]
    cdef int c1, r1, s = 0
    for c1 in range(1, N+1):
        r1 = sol[c1 - 1]
        if var != c1 and attacks(row, var, r1, c1):
            s += 1
    return s


cdef int select_value(int var, np.ndarray[np_type, ndim=1] current) except -1:
    cdef np.ndarray[np_type, ndim=1] conflicts_vec = np.zeros(N, dtype=DTYPE)
    cdef np.ndarray[np_type, ndim=1] current_o = current.copy()
    cdef int val
    for val in range(1, N + 1):
        set_value(current_o, var, val)
        conflicts_vec[val - 1] = num_of_conflicts(current_o, var)
        current_o = current.copy()
    return conflicts_vec.argmin() + 1


cpdef object min_conflicts(int n, int max_passi, int factor=-1):
    global N
    N = n
    cdef np.ndarray[np_type, ndim=1] current = start(factor)
    cdef int last = 0, cf = 0, i, it_count, var
    if max_passi < 0:
        max_passi = 100000000

    for it_count in range(max_passi):
        if factor > 0 and it_count % factor == 0:
            cf = 0
            for i in range(1, N + 1):
                cf += num_of_conflicts(current, i)
            print("Iteration", it_count, " # conflicts = ", cf)
            print(current)

        var = find_conflict_var(current, last)
        if var < 0:
            return current, it_count
        last = var
        val = select_value(var, current)
        set_value(current, var, val)
    return None, max_passi