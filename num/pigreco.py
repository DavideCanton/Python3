__author__ = 'davide'

from decimal import Decimal as D, getcontext
import math


def pi_greco(ks):
    p = D(0)
    for k in range(ks):
        f = D(1 / 16 ** k)
        a1 = D(4) / D(8 * k + 1)
        a2 = D(2) / D(8 * k + 4)
        a3 = D(1) / D(8 * k + 5)
        a4 = D(1) / D(8 * k + 6)
        p += f * (a1 - a2 - a3 - a4)
    return p


if __name__ == "__main__":
    getcontext().prec = 500
    k = 100
    p = pi_greco(k)
    print(math.pi == p)
    print(math.pi)
    print(p)