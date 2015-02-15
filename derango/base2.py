from math import floor

__author__ = 'davide'


def toBase2(f, l=32):
    i = floor(f)
    d = f - i
    res = []
    for _ in range(l):
        d *= 2
        res.append(str(int(d >= 1)))
        if d >= 1:
            d -= 1
    return str(i) + "." + "".join(res)


def fromBase2(s):
    si, sd = s.split(".")
    i = int(si, 2)
    m = .5
    d = 0
    for s in sd:
        if s == "1":
            d += m
        m /= 2
    return i + d

if __name__ == "__main__":
    s = input("Numero>")
    print(fromBase2(s))