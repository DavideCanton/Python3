__author__ = 'davide'


def g(n):
    yield from range(n, 0, -1)
    yield from range(0, n + 1)

if __name__ == "__main__":
    print(list(g(10)))