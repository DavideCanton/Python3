__author__ = 'davide'

import math
import numpy as np

sign = lambda x: -1 if near(x, 0) else math.copysign(1, x)
step = lambda x: int((sign(x) + 1) / 2.)


class avoid_overflow:
    def __init__(self, def_value):
        self.def_value = def_value

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except OverflowError:
                return def_value

        return wrapper


class ActFunction:
    def __call__(self, *args, **kwargs):
        raise NotImplemented

    def deriv(self, *args, **kwargs):
        raise NotImplemented

    def evaluate(self, x):
        return x > 0.5


def near(x, y, eps=1E-8):
    return abs(x - y) <= eps


class SigmoidActivator(ActFunction):
    def __init__(self, rate=1):
        self.rate = rate

    @avoid_overflow(0.)
    def __call__(self, x):
        return 1 / (1 + np.exp(-x * self.rate))

    def deriv(self, x):
        return x * (1 - x) * self.rate


class TanHActivator(ActFunction):
    def __call__(self, x):
        return np.tanh(x)

    def deriv(self, x):
        return 1.0 - x ** 2


class StepActivator(ActFunction):
    def __call__(self, x):
        if x > 0:
            return 1.
        elif x < 0:
            return 0.
        else:
            return 0.5

    def deriv(self, x):
        return 1