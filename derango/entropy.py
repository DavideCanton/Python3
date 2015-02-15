__author__ = 'davide'

import numpy as np
from math import log2
import matplotlib.pyplot as plt

vlog2 = np.vectorize(log2)


def H(p):
    return sum(p * vlog2(1 / p))


def near(x, y, c=1E-6):
    return abs(x - y) <= c


def g():
    n = 1
    p = np.array([4 / 25, 4 / 25, 10 / 25, 7 / 25])
    H1 = H(p)
    print("H1 =", H1)

    Hlist = [H1]
    pi = p
    for i in range(2, n + 1):
        pi = np.dstack(np.meshgrid(p, pi)).reshape(-1, 2)
        pi = np.prod(pi, axis=1)
        Hi = H(pi)
        print("H{} =".format(i), Hi)
        print(near(H1 * i, Hi))
        Hlist.append(Hi)

    x = np.arange(1, n + 1, 1)
    plt.plot(x, Hlist)
    plt.show()

if __name__ == "__main__":
    p1 = np.array([.16, .16, .4, .28]) / 3
    p2 = np.array([.2, .3, .5]) * 2 / 3

    pi = np.hstack([p1, p2])
    print(H(pi))

    pi2 = np.dstack(np.meshgrid(pi, pi)).reshape(-1, 2)
    pi2 = np.prod(pi2, axis=1)
    print(H(pi2))