__author__ = 'davide'

cimport numpy as np
import numpy as np

DTYPE = np.int
ctypedef np.int_t DTYPE_t

def collatz(int n):
    cdef np.ndarray[DTYPE_t, ndim=1] b = np.zeros(1000, dtype=DTYPE)
    cdef int i = 0

    while n > 1:
        b[i] = n
        i += 1
        if n & 1:
            n = 3 * n + 1
        else:
            n //= 2
    b[i] = 1
    return b[:i+1]