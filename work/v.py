__author__ = 'Kami'

from numba import jit, u8
import numpy as np
from timeit import default_timer as timer


@jit(u8(u8[:], u8[:]), nopython=True)
def f(v, v2):
    n = len(v)
    x = 0

    for i in range(n):
        for j in range(n):
            x += v[i] * v2[j]

    return x


def f2(v, v2):
    return np.sum(v[:, np.newaxis] * v2)


if __name__ == "__main__":
    v = np.random.random_integers(1, 10, 100).astype(dtype=np.uint64)
    v2 = np.random.random_integers(1, 10, 100).astype(dtype=np.uint64)
    start = timer()
    x = f(v, v2)
    print(timer() - start)
    print(x)

    #start = timer()
    #x = f2(v, v2)
    #print(timer() - start)
    #print(x)