import itertools as it
from collections import defaultdict

__author__ = 'Davide'

GRAPH_STR = """75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23"""


class Node:
    def __init__(self, i, j, n):
        self.i = i
        self.j = j
        self.n = int(n)

    def __hash__(self):
        return self.i * 17 + self.j * 53 + self.n * 19

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j and self.n == other.n

    def __str__(self):
        return "<{},{},{}>".format(self.i, self.j, self.n)


def build_graph(t):
    graph = defaultdict(list)
    current_level = None
    root = None
    ind = 0

    for ind, level in enumerate(t.split("\n")):
        if current_level is None:
            current_level = level.split()
            root = Node(0, 0, current_level[0])
        else:
            level = level.split()
            for i in range(len(current_level)):
                cur_node = Node(ind - 1, i, current_level[i])
                graph[cur_node].append(Node(ind, i, level[i]))
                graph[cur_node].append(Node(ind, i + 1, level[i + 1]))
            current_level = level

    return graph, root, ind


def edges(graph):
    for n in graph:
        for m in graph[n]:
            yield (n, m)


def find_max_path(graph, root, max_i):
    end = Node(max_i + 1, 0, 0)
    vals = set(it.chain.from_iterable(graph.values()))
    all_nodes = [n for n in set(graph.keys()) | vals]
    no_out = [n for n in all_nodes if n.i == max_i]
    for node in no_out:
        graph[node].append(end)
    all_nodes.append(end)

    father = {}
    dist = defaultdict(lambda: float("inf"))
    dist[root] = -root.n

    for i in range(len(all_nodes)):
        for (u, v) in edges(graph):
            alt = dist[u] - v.n
            if alt < dist[v]:
                dist[v] = alt
                father[v] = u

    cur_node = end
    path = []
    while True:
        path.append(cur_node)
        try:
            cur_node = father[cur_node]
        except KeyError:
            break
    return path[1:]


def main():
    graph, root, lev_cnt = build_graph(GRAPH_STR)

    for k, v in graph.items():
        assert len(v) == 2

    path = find_max_path(graph, root, lev_cnt)
    print(*path)
    print(sum(int(s.n) for s in path))


if __name__ == "__main__":
    main()
