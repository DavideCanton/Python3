__author__ = 'davide'

import functools
from fractions import Fraction

import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return abs(x ** 3 - 4 * x)


s = [-2, 0, 2]
d = len(s) - 1
x = np.r_[-2:2:100j]
fv = np.vectorize(f)
pol = np.polyfit(s, fv(s), d)
c = list(map(lambda x: Fraction(x).limit_denominator(), pol))
p = np.poly1d(pol)

fmt = r"\frac{{{0.numerator}}}{{{0.denominator}}}*x^{1}"
st = " + ".join(fmt.format(ci, d - i) for i, ci in enumerate(c) if ci)
plt.title("$" + (st or "0") + "$")
plt.plot(x, fv(x), label="f(x)")
plt.plot(x, p(x), label="p(x)")
plt.legend()
plt.show()
