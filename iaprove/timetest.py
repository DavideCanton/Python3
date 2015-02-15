from datetime import datetime
import itertools as it
from iaprove.impl_v import ArrayV
from random import randint


class timeit:
    def __init__(self, p):
        self.p = p

    def __call__(self, func):
        def wrapper(*a, **k):
            t = datetime.now()
            val = func(*a, **k)
            delta = datetime.now() - t
            af = ", ".join(map(str, a))
            kf = ", ".join("{}={}".format(k, v) for k, v in k.items())
            args = ", ".join((af, kf))
            if self.p:
                print("Call to {}({}) took {} ms"
                .format(func.__name__, args, delta.microseconds / 1000))
            return delta.microseconds / 1000, val

        return wrapper


@timeit(False)
def insert(v, coalition, val):
    v[coalition] = val


@timeit(False)
def get(v, coalition):
    return v[coalition]


def generateSubsets(vars):
    vars = sorted(vars)
    yield []
    for r in range(1, len(vars)):
        for subset in it.combinations(vars, r):
            yield list(subset)
    yield vars


if __name__ == '__main__':
    n = 15
    v = ArrayV(n)
    ins_time = 0
    for s in generateSubsets(list(range(n))):
        t, _ = insert(v, s, randint(0, 10))
        ins_time += t
    print("AVG Insert time=", ins_time / (2 ** n))
    get_time = 0
    for s in generateSubsets(list(range(n))):
        t, _ = get(v, s)
        get_time += t
    print("AVG Get time=", get_time / (2 ** n))
