__author__ = 'Davide'

import numpy as np


def mybin(n):
    l = 8
    neg = bool(n < 0)

    if n < 0:
        n = -n
    if n < 0:  # min val
        return "1" + "0" * (l - 1)

    res = []
    while n:
        rem = n % 2
        res.append(rem)
        n >>= 1

    if neg:
        res += [0] * (l - len(res))
        res = [1 - r for r in res]

        i = 0
        while i < l and res[i] == 1:
            res[i] = 0
            i += 1
        if i < l:
            res[i] = 1

    return "".join(map(str, reversed(res))).rjust(l, "0")


if __name__ == "__main__":
    m = {}

    for i in range(256):
        for j in range(256):
            ii = np.int8(i)
            jj = np.int8(j)
            rr = ii + jj

            OF_1 = int(ii < 0 and jj < 0 < rr or ii > 0 and jj > 0 > rr)

            if OF_1:
                # print(ii, jj, rr)
                # print(mybin(ii), mybin(jj), mybin(rr))
                pass

            a = mybin(ii)[:4]
            b = mybin(jj)[:4]
            c = mybin(rr)[:4]
            m.setdefault(OF_1, set()).add((a + b + c))

    print(m)
    print(m[0] & m[1])
