from collections import defaultdict
import pathlib

TOP = []


def add_edge(top, n1, n2):
    top.append((n1, n2))


def empty(top):
    return not top


def remove_leaves(top):
    nd = defaultdict(int)
    for (a, b) in top:
        nd[a] += 1
        nd[b] += 1
    leaves = {n for n, v in nd.items() if v == 1}
    return [(a, b)
            for (a, b) in top
            if a not in leaves and b not in leaves]


def main():
    global TOP

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
            TOP = remove_leaves(TOP)
            i += 1
        print(i)


if __name__ == "__main__":
    main()