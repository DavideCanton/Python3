from multiprocessing import Pool
import numpy as np


def f(x, a, b):
    return sum(i * x + b for i in a)


class G:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, x):
        return f(x, self.a, self.b)


if __name__ == '__main__':
    p = Pool(3)
    a = np.arange(0, 100)
    b = 10

    rl = p.map_async(G(a, b), range(20))
    print(rl.get())
