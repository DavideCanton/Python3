from tree import BinaryTree
from datetime import *


def timeit(func):
    def wrapper(*a, **k):
        t = datetime.now()
        val = func(*a, **k)
        delta = datetime.now() - t
        af = ", ".join(map(str, a))
        kf = ", ".join("{}={}".format(k, v) for k, v in k.items())
        args = ", ".join((af, kf))
        print("Call to {}({}) took {} ms"
              .format(func.__name__, args, delta.microseconds / 1000))
        return val
    return wrapper


@timeit
def search(tree, val):
    return tree._search(val)


def main():
    import sys
    sys.setrecursionlimit(1000000000)
    N = 1000
    tree = BinaryTree.buildTree(*range(N))
    for i in range(N):
        tree.add(i)
    for i in range(N):
        search(tree, i)


if __name__ == '__main__':
    main()
