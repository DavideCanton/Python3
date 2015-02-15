__author__ = 'davide'

import multiprocessing as mp
import time

n = mp.Value('i', 0)

def work():
    global n
    n.value += 1

if __name__ == "__main__":
    p = mp.Pool(3)

    n2 = [0]

    def cb(v):
        n2[0] += 1

    for _ in range(10000):
        p.apply_async(work, callback=cb)

    p.close()
    p.join()

    print(n.value, '/', n2[0])