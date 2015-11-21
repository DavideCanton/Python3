from operator import itemgetter

__author__ = 'davide'


def pairwise(l):
    for t in zip(l, l[1:]):
        yield t


def pijavskij(f, L, a, b, eps=1E-5):
    l = [(a, f(a)), (b, f(b))]

    while True:
        imin, Rmin, xmin = -1, float("inf"), -1
        for i, t in enumerate(pairwise(l)):
            (xi, fi), (xj, fj) = t
            R = (fi + fj - L * (xj - xi)) / 2
            if R < Rmin:
                imin = i
                Rmin = R
                xmin = (xi + xj) / 2 - (fj - fi) / (2 * L)
        if l[imin + 1][0] - l[imin][0] < eps:
            return l[imin], l[imin + 1]

        l.append((xmin, f(xmin)))
        l.sort(key=itemgetter(0))
        print(l)

if __name__ == "__main__":
    f = lambda x: x ** 4
    t = pijavskij(f, 50, -100, 100, eps=1E-10)
    print(t)
