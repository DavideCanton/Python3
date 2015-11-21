import functools
import operator
from math import factorial
from fractions import Fraction

__author__ = 'Davide'


def multinomial(n, ks):
    return factorial(n) / (functools.reduce(operator.mul,
                                            map(factorial, ks), 1))


def get_prob_1D(n, k):
    return multinomial(n, [(n - k) // 2, (n + k) // 2]) / 2 ** n


def get_prob0_2D(n):
    return 1 / (4 ** n) * sum(multinomial(n, [i, i, n // 2 - i, n // 2 - i])
                              for i in range(0, n // 2 + 1))


if __name__ == "__main__":
    for n in range(0, 20, 2):
        f = Fraction(get_prob0_2D(n))
        print(n, f)