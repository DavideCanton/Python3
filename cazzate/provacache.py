import functools
import random


@functools.lru_cache(maxsize=None)
def fib_cached(n):
    if n < 0:
        raise ValueError(str(n))
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


@functools.lru_cache(maxsize=None)
def fatt_cached(n):
    if n < 0:
        raise ValueError(str(n))
    if n < 2:
        return n
    return n * fatt_cached(n - 1)


@functools.lru_cache(maxsize=None)
def double_fatt_cached(n):
    if n < 0:
        raise ValueError(str(n))
    if n < 2:
        return n
    return n * fatt_cached(n - 2)

n = 20
r = list(range(n))

for f in (fatt_cached, fib_cached, double_fatt_cached):
    random.shuffle(r)
    list(map(f, r))
    info = f.cache_info()
    print(info)
    hits = info.hits
    misses = info.misses
    hits = hits / (hits + misses) * 100
    print("Rate {}: {:0.2f}% hits {:0.2f}% misses" \
          .format(f.__name__, hits, 100 - hits))
    print(f(n - 1))
