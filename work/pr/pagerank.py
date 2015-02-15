__author__ = 'Kami'

import numpy as np
import igraph
import multiprocessing.pool
from numba import jit, f8, i8
from timeit import default_timer as timer


@jit(f8[:](f8[:, :], f8, f8[:], i8))
def pagerank(A, alpha, v, iters):
    """pagerank originale -> OK """
    N = A.shape[0]
    x = np.ones_like(v) / N

    for _ in range(iters):
        x_old = x
        x = alpha * np.dot(A, x) + (1 - alpha) * v
        if np.allclose(x_old, x):
            break
    return x


@jit(f8[:](f8[:, :], f8, f8[:], i8))
def dirich_pr(A, mu, v, iters):
    N = A.shape[0]
    x = np.ones_like(v) / N
    omega = mu / (A.sum(axis=0) + mu)
    # omega /= omega.sum()
    A *= (1 - omega)[:, np.newaxis]

    for _ in range(iters):
        x_old = x
        x = np.dot(A, x) + np.dot(x, omega) / N
        if np.allclose(x_old, x):
            break
    return x


def init():
    N = 600
    g = igraph.Graph.Erdos_Renyi(N, m=int(N * 3), directed=True, loops=False)
    # g = igraph.Graph.Static_Power_Law(N, int(N * 1.5),
    # exponent_in=2.5, exponent_out=2.5)

    g.add_vertex(N)
    g.add_edge(N - 1, N)
    k = 30
    for i in range(N + 1, N + 1 + k):
        g.add_vertex(i)
        g.add_edge(N, i)
        g.add_edge(i, N)

    # igraph.plot(g)

    A = np.array(g.get_adjacency().data, dtype=np.float64)

    sums = A.sum(1)
    sums[sums == 0] = 1
    A /= sums[:, np.newaxis]

    v = np.ones(A.shape[0])
    v /= v.sum()

    return A, v, A.shape[0]


def init2():
    N = 31
    g = igraph.Graph(directed=True)
    # g = igraph.Graph.Static_Power_Law(N, int(N * 1.5),
    # exponent_in=2.5, exponent_out=2.5)

    for i in range(N):
        g.add_vertex(N)

    mid = (N - 1) // 2

    for i in range(mid):
        g.add_edge(i, mid)
        g.add_edge(mid, i + 1 + mid)

    # igraph.plot(g)

    A = np.array(g.get_adjacency().data, dtype=np.float64)
    sums = A.sum(1)
    sums[sums == 0] = 1
    A /= sums[:, np.newaxis]

    v = np.ones(A.shape[0])
    v /= v.sum()

    return A, v, A.shape[0]


if __name__ == "__main__":
    A, v, N = init()

    mask = np.where(A.sum(axis=1) == 0)[0]
    A[mask, :] = 1 / N

    start = timer()
    x = pagerank(A.T, .85, v, 1000)
    y = dirich_pr(A.T, 20., v, 1000)
    print(timer() - start)

    print("Node", "PR", "DR", sep="\t")
    for i, xi, yi in zip(range(N), x, y):
        print(i, xi, yi, sep="\t")

    print("Sum", x.sum(), y.sum(), sep="\t")