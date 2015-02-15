from itertools import product
from random import random
from math import copysign
# from cazzate.mybinary import bin_args
from fractions import Fraction, gcd
from functools import reduce
import numpy as np

near = lambda x, y: abs(x - y) <= 1E-8
sign = lambda x: 0 if near(x, 0) else copysign(1, x)
step = lambda x: int((sign(x) + 1) / 2.)


class Percettrone:
    def __init__(self, w_len, learning_rate=.5, func=step):
        self.l_rate = learning_rate
        self.w = np.zeros(w_len + 1)
        self.f = func

    def train(self, training_set):
        err = True
        while err:
            err = False
            for t in training_set:
                y = t[1]
                x = np.zeros(len(t[0]) + 1)
                x[:len(t[0])] = t[0]
                x[-1] = 1
                yp = self.f(np.dot(self.w, x))
                error = y - yp
                if error != 0:
                    err = True
                    self.w += self.l_rate * error * x

    def normalize(self):
        fl = [abs(Fraction.from_float(f).limit_denominator().denominator)
              for f in self.w]
        mcm = reduce(lambda a, b: a * b / gcd(a, b), fl)
        self.w = [int(w * mcm) for w in self.w]
        mcd = reduce(gcd, map(abs, self.w))
        if mcd:
            self.w = [w // mcd for w in self.w]

    def evaluate(self, input):
        input = list(input) + [1]
        return self.f(np.dot(input, self.w))


def make_f(s, n):
    def f(*args):
        l = locals()
        for ch, v in zip("abcdefghijklmnopqrstuvwxyz", args):
            l[ch] = v
        return int(eval(s, {"__builtins__": {}}, l))

    return f

if __name__ == '__main__':
    n = int(input("n>"))
    m = int(input("m>"))
    p = Percettrone(n)
    # f = lambda a, b, c: int(not (a and b and c)]
    # ts = [(s, f(*s)) for s in bin_args(n)]
    s = input("func>")
    f = make_f(s, n)
    ts = [(list(s), f(*s)) for s in product(range(m * n), repeat=n)]
    p.train(ts)
    print("Pesi non normalizzati:", p.w)
    p.normalize()
    print("Pesi normalizzati:", p.w)
    print("Classificazione training set:")
    res = True
    for t, e in zip(product(range(m * n), repeat=n), ts):
        pred = p.evaluate(t)
        expected = e[1]
        res &= pred == expected
        print(t, pred, expected, pred == expected, sep='\t' * 4)
    print("Risultato:", res)
    print("Classificazione random:")
    res = True
    falses = []
    for _ in range(10):
        c = list(map(int, [random() * m for _ in range(n)]))
        r, t = f(*c), p.evaluate(c)
        res &= r == t
        if r != t:
            falses.append(c)
            print(c, r, t, r == t, sep='\t' * 4)
    print("Risultato:", res)
    print("\n".join(map(str, falses)))
