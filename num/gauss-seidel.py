__author__ = 'davide'

import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Solver:
    def __init__(self, start_x=None):
        self.done = False
        self.x = start_x
        self.it = None

    def set_params(self, A, b):
        self.A = A
        self.b = b

    def _iterate(self):
        d = len(b)
        if self.x is None:
            self.x = np.zeros(d)
        while not self.done:
            xn = np.zeros(d)
            for i in range(d):
                xn[i] = Solver.compute_x(i, self.x, xn,
                                         self.A[i], self.b[i])
            self.x = xn
            yield xn

    def iterate_sol(self):
        yield from self._iterate()

    def reset(self):
        self.done = False

    def end(self):
        self.done = True

    @staticmethod
    def compute_x(i, x_old, x_new, row, b):
        s1 = np.dot(row[:i], x_new[:i])
        s2 = np.dot(row[i + 1:], x_old[i + 1:])
        return (b - s1 - s2) / row[i]


def not_stable(A):
    M = np.tril(A)
    N = np.triu(A)
    N[np.diag_indices_from(N)] = 0.
    B = np.dot(np.linalg.inv(M), -N)
    l, _ = np.linalg.eig(B)
    return max(abs(l)) >= 1


if __name__ == "__main__":
    N = 3

    b = np.random.rand(N) * 10 - 5
    while True:
        A = np.random.rand(N, N) * 10 - 5

        if np.count_nonzero(A) == 0:
            exit("Matrice nulla")
        # if 0 in np.diag(A):
        # print("Scambio")
        # A = A[[1, 0]]

        # if not_stable(A):
        # exit("Metodo non stabile")
        # print("Non stabile!")

        if not not_stable(A):
            break

    print("A matrix:")
    print(A)

    print("rhs vector:")
    print(b)
    start_x = b
    s = Solver(start_x)
    s.set_params(A, b)
    x, y, z = [], [], []
    P = 10
    L = deque([start_x], maxlen=P)

    for rx, _ in zip(s.iterate_sol(), range(100000)):
        last = L[-1]
        L.append(rx)

        x.append(rx[0])
        y.append(rx[1])
        try:
            z.append(rx[2])
        except IndexError:
            z.append(0)

        if np.allclose(last, rx):
            break

    s.end()
    sol = L[-1]
    print("Solution:")
    print(sol)
    error = np.dot(A, sol) - b
    print("Error:")
    print(error)
    if np.linalg.norm(error) > 1e8:
        print("ERROR!")

    fig = plt.figure()
    plt.title(
        "Iteration of Gauss-Seidel Method with A={} and b={}".format(A, b))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, "bo-")
    plt.show()