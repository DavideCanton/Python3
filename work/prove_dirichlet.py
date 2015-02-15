__author__ = 'Kami'

import numpy as np


def partition(s, a):
    c = 0
    l = []
    for v in a:
        if v:
            l.append(s[c:c + v])
            c += v
    return l


if __name__ == "__main__":
    s = "ciao sono davide"
    a = np.array([1, 1, 1])
    a = a / a.sum()

    for _ in range(10):
        b = np.random.dirichlet(a)
        b *= len(s)
        b = np.around(b).astype(np.uint8)
        if b.sum() < len(s):
            b[-1] += 1
        p = partition(s, b)
        print(b, "->", p)