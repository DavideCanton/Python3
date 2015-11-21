import multiprocessing.pool as mp_pool
import functools
import time
import random


def f(x, a, b):
    span = random.randint(1, 3)
    time.sleep(span)
    return sum(i * x + b for i in a)


if __name__ == '__main__':
    with mp_pool.Pool(processes=10) as pool:
        a = list(range(10))
        b = 10
        func = functools.partial(f, a=a, b=b)
        result_list = [pool.apply_async(func, [i]) for i in range(20)]
        for result in result_list:
            print(result.get())
