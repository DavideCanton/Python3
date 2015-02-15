__author__ = 'Kami'

from funcdep import FuncDep, keys_of, reduce_set, merge
from random import random, randint, sample, seed
from string import ascii_uppercase
import sys


def load_set(path):
    func_set = set()
    with open(path) as f:
        attlist = set(next(f).strip().split())
        for line in f:
            line = line.strip()
            if not line:
                continue
            l, r = [set(s.strip().split()) for s in line.split("->")]
            func_set.add(FuncDep(l, r))
    return attlist, func_set


if __name__ == '__main__':
    path = sys.argv[1]

    attlist, func_set = load_set(path)
    print("Original FD set:")
    func_set = merge(func_set)
    print(func_set)
    old_len = len(func_set)

    func_set = reduce_set(func_set)
    print("Reduced FD set:")
    print(func_set)

    keys = set("".join(k) for k in keys_of(attlist, func_set))
    print("Keys:")
    print(keys)
    print("Removed {} dependencies".format(old_len - len(func_set)))