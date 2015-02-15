from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

__author__ = 'davide'


def log2(x):
    return np.log(x) / np.log(2)


def get_S_delta(l, delta):
    l = sorted(l, reverse=True)
    r = 0
    v = 0
    for el in l:
        v += el
        r += 1
        if v >= 1 - delta:
            break
    return r


def H_delta(p, delta):
    return log2(get_S_delta(p, delta))


def get_X_N(p0, p1, n):
    l = []
    for i in range(2 ** n):
        b = np.binary_repr(i, n)
        m = np.array(list(b), dtype='i')
        ones = np.count_nonzero(m)
        l.append(p0 ** (n - ones) * p1 ** ones)
    return l


def get_H_delta_X_N(p0, p1, n, delta, global_stop):
    if global_stop.is_set():
        return 0
    print(mp.current_process().name, "executing with delta =", delta)
    v = H_delta(get_X_N(p0, p1, n), delta)
    if v == 0:
        global_stop.set()
    return v


if __name__ == "__main__":
    p0 = .9
    p1 = .1

    N = 10

    delta = np.linspace(0, 1.0, 10)
    res = []

    manager = mp.Manager()
    global_stop = manager.Event()

    pool = mp.Pool(mp.cpu_count() * 2)

    for d in delta:
        f = pool.apply_async(get_H_delta_X_N,
                             (p0, p1, N, d, global_stop))
        res.append(f)

    pool.close()
    y = np.array([e.get() for e in res])
    plt.step(delta, y, label="N={}".format(N))

    plt.legend()
    plt.show()