__author__ = 'davide'

from collections import defaultdict
import itertools as it
import random


if __name__ == "__main__":
    ID = 0

    def factory():
        global ID
        val = ID
        ID += 1
        return val

    diz = defaultdict(factory)
    l = list("abcd") * 3
    random.shuffle(l)
    for s in l:
        print(s, diz[s])