from bd.funcdep import FuncDep, keys_of, reduce_set, merge
from random import random, randint, sample, seed
from string import ascii_uppercase

if __name__ == '__main__':
    s = int(random() * 3982958239)
    print("*** USING SEED = {} ***".format(s))
    seed(s)
    limit_att = randint(3, 8)
    limit = 6
    left = 3
    right = 3
    attlist = ascii_uppercase[:limit_att]
    print("Attributi: {}".format(attlist))
    func_set = set()
    for _ in range(limit):
        nl = min(randint(1, left), len(attlist))
        nr = min(randint(1, right), len(attlist))
        fd = FuncDep(sample(attlist, nl), sample(attlist, nr))
        if fd.right:
            func_set.add(fd)
    print(func_set)
    func_set = merge(func_set)
    print(func_set)
    old_len = len(func_set)
    lk_a = set("".join(k) for k in keys_of(attlist, func_set))
    func_set = reduce_set(func_set)
    print(func_set)
    lk_b = set("".join(k) for k in keys_of(attlist, func_set))
    assert lk_a == lk_b
    print(lk_a)
    print(lk_b)
    print("Removed {} dependencies".format(old_len - len(func_set)))