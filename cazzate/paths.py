import itertools as it

__author__ = 'Kami'


def U(x, y):
    return x, y - 1


def D(x, y):
    return x, y + 1


def L(x, y):
    return x - 1, y


def R(x, y):
    return x + 1, y


def get_prob(n, k):
    s, tot = 0, 0
    for path in it.product([U, D, L, R], repeat=n):
        pos = 0, 0
        for fun in path:
            pos = fun(*pos)
        if abs(pos[0]) + abs(pos[1]) == k:
            s += 1
            # print("".join(f.__name__ for f in path))
        tot += 1
    return s, tot


if __name__ == "__main__":
    d = {(n, k): get_prob(n, k)
         for n in range(1, 10)
         for k in [1] if n & 1 == k & 1}
    for k, v in d.items():
        a, b = k
        n, d = v
        print(k, "->", "{}/{}".format(n, d))
