__author__ = 'Kami'

from numba import jit, u8, void
import numpy as np
from timeit import default_timer as timer


def make_fib(b):
    for i in range(2, b.shape[0]):
        b[i] = b[i - 1] + b[i - 2]


if __name__ == "__main__":
    make_fib_jit = jit(void(u8[:]))(make_fib)
    n = 20000

    b = np.zeros(n, dtype=np.uint64)
    b[1] = 1
    start = timer()
    make_fib(b)
    print("1st:", timer() - start)

    b = np.zeros(n, dtype=np.uint64)
    b[1] = 1
    start = timer()
    make_fib_jit(b)
    print("2nd:", timer() - start)

