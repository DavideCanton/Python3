from multiprocessing.pool import Pool

from euler._utils import genera_primi

__author__ = 'Kami'


def divisors_num(n):
    r = 1
    n_orig = n
    for p in genera_primi():
        c = 0
        while n % p == 0:
            n //= p
            c += 1
        r *= 1 + c
        if p * p > n_orig:
            break

    return r


if __name__ == "__main__":
    with Pool(8) as pool:

        triangle_numbers = [n * (n + 1) >> 1 for n in range(1, 70000)]
        results = pool.imap(func=divisors_num, iterable=triangle_numbers,
                            chunksize=10)

        for n, res in zip(triangle_numbers, results):
            if res > 500:
                print(n)
                pool.terminate()
                exit()
