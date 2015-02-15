__author__ = 'davide'

import random


def log(fun):
    n = 0

    def wr(*a, **kw):
        nonlocal n

        print("{}>Called function({})".format(n, a[0]))
        n += 1
        ret = fun(*a, **kw)
        n -= 1
        print("{}>{}".format(n, ret))
        return ret

    return wr


@log
def qsort(l):
    if len(l) <= 1:
        return l
    p = random.choice(l)
    l1, l2, l3 = [], [], []
    for el in l:
        if el < p:
            l1.append(el)
        elif el == p:
            l2.append(el)
        else:
            l3.append(el)
    return qsort(l1) + l2 + qsort(l3)


if __name__ == "__main__":
    l = [0, 1, 5, 2, 1, 2]
    l = qsort(l)
    print(l)