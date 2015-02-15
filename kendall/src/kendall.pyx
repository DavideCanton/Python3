__author__ = 'davide'

import numpy as np

cimport numpy as np
cimport cython

ctypedef np.uint32_t DTYPE_T

@cython.boundscheck(False)
cpdef double kendall_distance(np.ndarray[DTYPE_T, ndim=1] a,
                              np.ndarray[DTYPE_T, ndim=1] b):
    cdef int n = a.shape[0]
    cdef np.ndarray[np.int64_t, ndim=1] ia = np.argsort(a)
    cdef np.ndarray[np.int64_t, ndim=1] ib = np.argsort(b)

    cdef int c = 0
    cdef int d = 0
    cdef int i, j

    for i in range(n):
        for j in range(i + 1, n):
            if ia[i] > ia[j] and ib[i] < ib[j]:
                d += 1
            elif ia[i] < ia[j] and ib[i] > ib[j]:
                d += 1
            else:
                c += 1

    return (c - d) / <double> (c + d)