import numpy as np
import numpy.random as nprand
import multiprocessing as mp


def simula():
    num = np.tile(np.arange(1, 11), 4)
    num = nprand.permutation(num)
    for i in [1, 2, 3]:
        mask = num[(i - 1)::3] == i
        if np.any(mask):
            return False
    return True


if __name__ == '__main__':
    max_t = 1000
    u = mp.Value("i")
    n = mp.cpu_count() * 2

    def callback(result):
        if result:
            with u.get_lock():
                u.value += 1

    p = mp.Pool(processes=n)
    for i in range(max_t):
        p.apply_async(simula, callback=callback)
    p.close()
    p.join()

    print("Uscito", u.value, "volte su", max_t)
    print("% =", u.value / max_t * 100)
