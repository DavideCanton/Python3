from neural.perceptron import Perceptron
from itertools import product
from random import random, sample, choice, randint
from fractions import Fraction, gcd
from functools import reduce
from utils import *
import string

__author__ = 'davide'


def normalize(w):
    frac_list = [abs(Fraction.from_float(element).limit_denominator().denominator)
                 for element in w]
    mcm = reduce(lambda a, b: a * b / gcd(a, b), frac_list)
    w = [int(x * mcm) for x in w]
    mcd = reduce(gcd, map(abs, w))
    if mcd:
        w = [x // mcd for x in w]
    return w


def make_f(func_string):
    def wrapper(*args):
        loc = locals()
        for ch, v in zip(string.ascii_lowercase, args):
            loc[ch] = v
        return int(eval(func_string, {"__builtins__": {}}, loc))

    return wrapper


def s_rand(a, b):
    return randint(a, b) * (-1 if random() > 0.5 else 1)


if __name__ == '__main__':
    n = 7
    max_v = 4
    factor = .65
    full_ts = list(product(range(max_v), repeat=n))
    sample_ts = sample(full_ts, int(len(full_ts) * factor))
    print(sample_ts)

    random_w = [s_rand(0, 100) for _ in range(n)]
    sign = choice([">", "<", ">=", "<="])
    rhs = randint(0, 100) * (-1 if random() > 0.5 else 1)
    s = "+".join(["({}*{})".format(a, b)
                  for a, b in zip(random_w, string.ascii_lowercase)])
    s += sign + str(rhs)
    print(s)
    f = make_f(s)

    p = Perceptron(n, learning_rate=100, momentum=.5, func=StepActivator())
    esito = p.train(sample_ts, f)

    if not esito:
        exit("Funzione non linearmente separabile!")
    print("Pesi:", p.weights)
    print("Classificazione sample training set:")

    res = True
    wrong = []
    for t in sample_ts:
        pred = p(t)
        expected = f(*t)
        correct = near(pred, expected)
        if not correct:
            wrong.append(t)
        res &= correct
        #print(t, pred, expected, correct, sep='\t' * 4)
    print("Risultato:", res)
    if not res:
        print(" ".join(map(str, wrong)))
    print("Classificazione full training set:")
    res = True
    wrong = []
    for t in full_ts:
        pred = p(t)
        expected = f(*t)
        correct = near(pred, expected)
        if not correct:
            wrong.append(t)
        res &= correct
        #print(t, pred, expected, correct, sep='\t' * 4)
    print("Risultato:", res)
    if not res:
        print(" ".join(map(str, wrong)))
    print("Classificazione random:")
    res = True
    falses = []
    for _ in range(int(len(full_ts) * factor)):
        c = list([int(random() * max_v) for _ in range(n)])
        r, t = f(*c), p(c)
        ok = near(r, t)
        res &= ok
        if not ok:
            falses.append(c)
            print(c, r, t, r == t, sep='\t' * 4)
    print("Risultato:", res)
    print(" ".join(map(str, falses)))
