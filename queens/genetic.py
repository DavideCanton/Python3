__author__ = 'davide'

from random import randint, random
import itertools as it
import bisect


def find_solution(population,
                  select, optimal,
                  crossover, mutation,
                  fitness, mutation_range, threshold, elite_size,
                  max_iterations=1000000):
    for iteration in range(max_iterations):
        new_pop = []
        print("Iterazione {}...".format(iteration))
        print("Popolazione di {} individui".format(len(population)))
        for _ in range(len(population)):
            x = select(population, fitness)
            if optimal(x):
                return x, iteration
            y = select(population, fitness)
            if optimal(y):
                return y, iteration
            z = crossover(x, y)
            if random() < random():
                z = mutation(z, mutation_range)
            new_pop.append(z)
            if optimal(z):
                return z, iteration + 1
        if len(new_pop) == 1:
            return new_pop[0], -1
            #elite = list(sorted(population, key=fitness)[-elite_size:])
        population = [x for x in new_pop if fitness(x) >= threshold]
        population = list(sorted(population, key=fitness)[-elite_size:])
    return max(population, key=fitness), -1


def crossover_1(x, y):
    p = randint(0, len(x) - 1)
    return x[:p] + y[p:]


def crossover_2(x, y):
    p = randint(0, len(x) - 1)
    q = randint(0, len(x) - 1)
    if p > q:
        p, q = q, p
    return x[:p] + y[p:q] + x[q:]


def mutation(x, mutation_range):
    p = randint(0, len(x) - 1)
    n = randint(*mutation_range)
    return x[:p] + (n,) + x[p + 1:]


def select(population, fitness):
    weights = list(map(fitness, population))
    cumdist = list(it.accumulate(weights))
    x = random() * cumdist[-1]
    return population[bisect.bisect(cumdist, x)]

