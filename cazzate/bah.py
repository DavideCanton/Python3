from random import random


class Trace:
    _funcs = {}

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self._funcs[self.func] = self._funcs.get(self.func, 0) + 1
        return self.func(*args, **kwargs)

    @staticmethod
    def count(f):
        # qua f e' un oggetto Trace non una funzione
        return f._funcs.get(f.func, 0)


@Trace
def spam(a, b, c):
    print(a + b + c)


@Trace
def spam2(a, b, c):
    print(a - b + c)


for _ in range(100):
    if random() >= 0.5:
        spam(1, 2, 3)
    else:
        spam2(1, 2, 3)
    print(Trace.count(spam), Trace.count(spam2))
