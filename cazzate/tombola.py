__author__ = 'Davide'

import numpy as np


def setup():
    def c(n):
        if n == 0:
            return np.r_[1:10, np.zeros(9)].reshape((-1, 1))
        elif n == 8:
            return np.r_[80:91, np.zeros(7)].reshape((-1, 1))
        else:
            return np.r_[n * 10:(n + 1) * 10, np.zeros(8)].reshape((-1, 1))

    return np.hstack([c(n) for n in range(9)])


def valid(a):
    for i in range(6):
        b = a[i * 3:(i + 1) * 3, :]
        if np.count_nonzero(b) != 15:
            return False

        nnz = np.apply_along_axis(lambda x: len(np.where(x != 0)[0]), 0, b)
        if np.any(nnz == 0):
            return False

    return True


def shuffle(a):
    for i in range(9):
        a[:, i] = a[np.random.permutation(range(18)), i]


def genera_cartelle():
    n = 0
    while True:
        a = setup()
        shuffle(a)
        if valid(a):
            return a
        n += 1


if __name__ == "__main__":
    print(genera_cartelle())
