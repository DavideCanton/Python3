__author__ = 'davide'

cdef int* C = [0, 3, 2, 2, 2, 2, 2, 4, 1, 4, 1, 3, 2, 2, 3, 4, 1, 2, 3, 3, 1, 1,
              3, 3, 2, 3, 2, 4, 3, 3, 4, 5]
cdef int* D = [0, 2, 1, 1, 2, 2, 2, 20, 1, 26, 1, 10, 4, 4, 13, 40, 2, 5, 17, 17, 2, 2,
     20, 20, 8, 22, 8, 71, 26, 26, 80, 242]

cpdef collatz_len(unsigned long long n):
    cdef unsigned long long l = 0, b
    while n > 1:
        b = n & 0x1F
        n = (n >> 5) * 3 ** C[b] + D[b]
        l += 5
    return l