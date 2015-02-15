__author__ = 'davide'

from functools import lru_cache
from math import factorial as fact
import matplotlib.pyplot as plt
import numpy as np
import functools as ft
from fractions import Fraction
import random


def density(x, a, b):
    return x ** a * (1 - x) ** b * fact(a + b + 1) / fact(a) / fact(b)


def from_string(s):
    na = s.count("a")
    return na, len(s) - na


def rstr():
    s = ["a"] * random.randint(1, 20) + ["b"] * random.randint(1, 20)
    random.shuffle(s)
    return "".join(s)


if __name__ == "__main__":
    s = rstr()
    a, b = from_string(s)
    print(s)
    x = np.linspace(0, 1, 1000)
    y = density(x, a, b)
    m = Fraction.from_float(x[np.argmax(y)]).limit_denominator()
    plt.suptitle("Max = {}".format(m), fontsize=20)
    plt.plot(x, y)
    plt.show()