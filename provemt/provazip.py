__author__ = 'davide'

from multiprocessing.pool import Pool
import itertools as it


def compute(x, y):
    return x + y


if __name__ == "__main__":
    p = Pool(3)
    res = p.starmap(compute, zip(it.count(), it.repeat(1, 10)))
    print(res)
    p.close()