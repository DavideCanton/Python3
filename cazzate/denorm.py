__author__ = 'Kami'

import fractions
import numpy as np
import functools


def denorm(x):
    if np.count_nonzero(x) == 0:
        return x
    limit = 100000
    while True:
        fr = [fractions.Fraction(v).limit_denominator(limit) for v in x]
        dens = [v.denominator for v in fr]
        max_den = max(dens)
        lcm = functools.reduce(lambda x, y: x * y / fractions.gcd(x, y), dens,
                               max_den)
        res = np.round(x * lcm)
        if np.linalg.norm(x - res) < 1e-6:
            return res
        if np.all(res < 100000):
            return res
        limit //= 10


def main():
    a = np.array(np.random.randint(1, 20000, 10), dtype=float)
    b = a.copy()
    b /= b.sum()
    print(b.sum())
    # b = np.round(b, 20)
    c = denorm(b)

    print(a)
    print(b)
    print(c)

    print(np.linalg.norm(a - c))
    print(c / c.sum())


if __name__ == "__main__":
    main()
