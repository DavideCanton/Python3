__author__ = 'davide'

import itertools as it
import numpy as np
from collections import defaultdict
from math import factorial
import operator


if __name__ == "__main__":
    REP = 1
    MAX = 3
    num = np.tile(np.arange(1, MAX + 1), REP)
    res = np.zeros(3)

    for p in it.permutations(num):
        valid = defaultdict(bool)
        for i in range(3):
            if len((num[i::3] == i + 1).nonzero()[0]):
                valid[i] = True

        for r in range(1, REP + 1):
            for s in it.combinations(range(3), r):
                if all(valid[x] for x in s):
                    res[r - 1] += 1

    res /= factorial(len(num))
    print(res)
