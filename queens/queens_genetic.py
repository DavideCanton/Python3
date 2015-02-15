__author__ = 'davide'

from random import randint
from functools import lru_cache
from genetic import find_solution, select, crossover_1, mutation

BOARD_SIZE = 12
MAX_FITNESS = BOARD_SIZE * (BOARD_SIZE - 1) / 2
THRESHOLD = MAX_FITNESS / 4
ELITE_SIZE = 50


@lru_cache()
def attacks(pos_1, pos_2):
    return (pos_1[0] == pos_2[0] or
            pos_1[1] == pos_2[1] or
            abs(pos_1[0] - pos_2[0]) == abs(pos_1[1] - pos_2[1]))


def print_board(positions):
    for i in range(BOARD_SIZE):
        print("|", end="")
        for j in range(BOARD_SIZE):
            if positions[j] == i:
                print("O", end="")
            else:
                print(" ", end="")
            print("|", end="")
        print()


@lru_cache()
def fitness(positions):
    return sum(not attacks((r1, c1), (r2, c2))
               for c1, r1 in enumerate(positions)
               for c2, r2 in enumerate(positions[c1 + 1:], start=c1 + 1)
               if c1 != c2)


def optimal(sol):
    return fitness(sol) == MAX_FITNESS


if __name__ == "__main__":
    def random_pos():
        return tuple(randint(0, BOARD_SIZE - 1)
                     for _ in range(BOARD_SIZE))

    population = [random_pos() for _ in range(100)]
    solution, iters = find_solution(population, select, optimal,
                                    crossover_1, mutation, fitness,
                                    [0, BOARD_SIZE - 1], THRESHOLD, ELITE_SIZE)
    print("Trovata!" if iters >= 0 else "Terminato timeout")
    print_board(solution)
    print(iters)