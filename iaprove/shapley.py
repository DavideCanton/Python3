from operator import mul
from functools import reduce
from itertools import permutations, combinations
from random import random
from iaprove.impl_v import ArrayV as V


def fact(n):
    if n == 0:
        return 1
    return reduce(mul, range(1, n + 1))


def compute_sv(n, v):
    sv = []
    nf = fact(n)
    for i in range(n):
        val = 0
        for r in permutations(range(n)):
            si_r = r[:r.index(i)]
            val += v[si_r + (i,)] - v[si_r]
        sv.append(val / nf)
    return sv

def subsets(n):
    I = list(range(0, n))

    for r in range(1, n):
        for subset in combinations(I, r):
            yield list(subset)

    yield I

if __name__ == '__main__':
    n = 10
    v = V(n)
    for s in subsets(n):
        v[s] = int(random() * 10)
        print("V({}) = {}".format(s, v[s]))
    sv = compute_sv(n, v)
    print(sv)
