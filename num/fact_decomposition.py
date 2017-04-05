import functools
import itertools as it
import heapq
import math
import operator

__author__ = 'Davide'


def primes():
    yield 2
    todel = [(4, 2)]
    n = 3
    while True:
        if todel[0][0] != n:
            yield n
            heapq.heappush(todel, (n * n, n))
        else:
            while todel[0][0] == n:
                p = todel[0][1]
                heapq.heapreplace(todel, (n + p, p))
        n += 1


def powers_of(p, start=0):
    return map(lambda k: p ** k, it.count(start))


def num_p(n, p):
    powers = powers_of(p, start=1)
    return sum(n // power for power in it.takewhile(lambda x: x <= n, powers))


def fact_decomposition(n):
    return [(p, num_p(n, p)) for p in it.takewhile(lambda x: x <= n, primes())]


def my_product(iterable):
    return functools.reduce(operator.mul, iterable, 1)


def main():
    n = 400000
    fact = math.factorial(n)

    decomposition = fact_decomposition(n)

    prod = my_product(it.starmap(operator.pow, decomposition))

    print(decomposition)
    print(list(it.starmap(operator.pow, decomposition)))

    assert prod == fact


if __name__ == "__main__":
    main()
