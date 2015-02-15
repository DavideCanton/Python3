def collatz(int n):
    cdef int l = 0

    while n > 1:
        l += 1
        if n & 1:
            n = 3 * n + 1
        else:
            n //= 2
    return l