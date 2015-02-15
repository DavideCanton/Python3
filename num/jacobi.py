from collections import deque

__author__ = 'davide'

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque
import itertools as it
from multiprocessing.pool import Pool


def compute_x(i, x, row, b):
    s1 = np.dot(row[:i], x[:i])
    s2 = np.dot(row[i + 1:], x[i + 1:])
    return (b - s1 - s2) / row[i]


class Solver:
    def __init__(self, start_x):
        self.pool = Pool(4)
        self.done = False
        self.x = start_x
        self.A = self.b = None

    def set_params(self, A, b):
        self.A = A
        self.b = b

    def iterate_sol(self):
        while not self.done:
            sol_iter = zip(it.count(), it.repeat(self.x), self.A, self.b)
            res = self.pool.starmap(compute_x, sol_iter)
            self.x = res
            yield np.array(res)

    def reset(self):
        self.done = False

    def end(self):
        self.done = True
        self.pool.close()


def unstable(A):
    B = -A.copy()
    B[np.diag_indices_from(B)] = 0
    B = np.einsum('ij,i->ij', B, 1 / np.diagonal(A))
    l, _ = np.linalg.eig(B)
    max_eig = np.abs(l).max()
    return max_eig >= 1


if __name__ == "__main__":
    N = 3

    while True:
        A = np.random.randn(N, N) * 100

        if np.count_nonzero(A) == 0:
            exit("Matrice nulla")

        if np.count_nonzero(np.diagonal(A)) != N:
            continue

        # print("A matrix:")
        # print(A)

        if not unstable(A):
            break

    b = np.random.rand(N) * 100 - 50
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

    for rx, _ in zip(s.iterate_sol(), range(1000)):
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

    plt.title("Iteration of Jacobi Method with A={} and b={}".format(A, b))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, "bo-")
    plt.show()