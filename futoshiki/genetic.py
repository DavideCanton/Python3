__author__ = 'davide'

from functools import partial, lru_cache
from random import randint, random, shuffle, sample
from math import sqrt
import collections
import itertools as it
import bisect
import numpy as np
from board import Board


THRESHOLD = 20
ELITE_SIZE = 100


def find_solution(population, original, N, max_iterations=1000000):
    fitness_p = partial(fitness, original=original, N=N)
    for iteration in range(max_iterations):
        new_pop = []
        print("Iterazione {}...".format(iteration))
        print("Popolazione di {} individui".format(len(population)))
        for _ in range(len(population)):
            x = select(population, fitness_p)
            if optimal(x, original):
                return x, iteration
            y = select(population, fitness_p)
            if optimal(y, original):
                return y, iteration
            z = crossover_u(x, y)
            if random() < random():
                z = mutation(z, original, N)
            if optimal(z, original):
                return z, iteration + 1
            new_pop.append(z)
        if len(new_pop) == 1:
            return new_pop[0], -1

        #elite = list(sorted(population, key=fitness_p)[-ELITE_SIZE:])
        population = [x for x in new_pop if fitness_p(x) >= THRESHOLD]
        #population = list(sorted(population, key=fitness_p)[-ELITE_SIZE:])
    return max(population, key=fitness_p), -1


def crossover(x, y):
    n = len(x)
    p = randint(0, n - 1)
    return x[:p] + y[p:]


def crossover_u(x, y, ratio=.5):
    n = len(x)
    p = int(ratio * n)
    indexes = set(sample(list(range(n)), p))
    z = [0] * n
    for i in range(n):
        z[i] = x[i] if i in indexes else y[i]
    return tuple(z)


def mutation(x, original, N):
    p = randint(0, N * N - 1)
    while divmod(p, N) in original.fixed:
        p = randint(0, N * N - 1)
    n = randint(1, N)
    return x[:p] + (n,) + x[p + 1:]


def select(population, fitness):
    weights = list(map(fitness, population))
    cumdist = list(it.accumulate(weights))
    x = random() * cumdist[-1]
    return population[bisect.bisect(cumdist, x)]


def board_to_array(board):
    return tuple(board.matrix.flatten())


def array_to_board(array, original):
    n = int(sqrt(len(array)))
    b = Board(n)
    b.matrix = np.array(array).reshape((n, n))
    b.constraints = original.constraints
    b.num_constr = original.num_constr
    b.fixed = original.fixed
    return b


@lru_cache()
def fitness(element, original, N):
    b = array_to_board(element, original)
    val = 0
    c_cols = [collections.Counter(b.matrix[:, i]) for i in range(N)]
    for i in range(N):
        c_row = collections.Counter(b.matrix[i, :])
        for j in range(N):
            el = b.matrix[i, j]
            val += 2 * N - c_row[el] - c_cols[j][el]
    return val + b.valid_constraints()


@lru_cache()
def optimal(sol, original):
    b = array_to_board(sol, original)
    return b.is_valid() and b.is_filled()

