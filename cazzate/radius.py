import pathlib
from collections import defaultdict

TOP = defaultdict(set)


def add_edge(top, n1, n2):
    top[n1].add(n2)
    top[n2].add(n1)


def empty(top):
    return all(not nodeset for nodeset in top.values())


def remove_leaves(top):
    leaves = {n for n, v in top.items() if len(v) == 1}
    for n in leaves:
        del top[n]
    for n in top:
        top[n] -= leaves


def main():
    with pathlib.Path("files/in.txt").open() as fp:
        n = 0
        m = int(fp.readline())  # the number of adjacency relations
        for i in range(m):
            xi, yi = [int(i) for i in fp.readline().split()]
            add_edge(TOP, xi, yi)
            n = max(n, xi, yi)
        n += 1

        i = 0
        while not empty(TOP):
            remove_leaves(TOP)
            i += 1
        print(i)


if __name__ == "__main__":
    main()