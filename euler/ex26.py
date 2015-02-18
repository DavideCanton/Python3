__author__ = 'davide'


def useless(n):
    while n % 2 == 0:
        n >>= 1
    while n % 5 == 0:
        n //= 5

    return n == 1


def period_len(n):
    r = 1
    for i in range(n):
        r = (r * 10) % n
    r0 = r
    l = 0
    r = r0
    while True:
        r = (10 * r) % n
        l += 1
        if r == r0:
            break
    return l


def main():
    ns = [(period_len(n), n) for n in range(2, 1000) if not useless(n)]
    m = max(ns)
    print(m)


if __name__ == "__main__":
    main()