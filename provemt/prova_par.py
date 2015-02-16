from multiprocessing import Pool
import numpy as np


def f(x, a, b):
    return sum(i * x + b for i in a)

if __name__ == '__main__':
    p = Pool(3)
    a = np.arange(0, 100)
    b = 10
    rl = [p.apply_async(f, (x, a, b)) for x in range(20)]
    for r in rl:
        print(r.get())
