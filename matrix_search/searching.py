import heapq as hq
from collections import deque
from functools import total_ordering
from random import shuffle

import numpy as np


@total_ordering
class Node:
    def __init__(self, content, parent=None, value=0, depth=0):
        self.content = content
        self.value = value
        self.depth = depth
        self.parent = parent

    def __eq__(self, val):
        return self.value == val.value

    def __lt__(self, val):
        return self.value < val.value

    def __repr__(self):
        return ("<Node, cnt: {}, val: {}, dpt: {}>"
                .format(self.content, self.value, self.depth))


class Info:
    def __init__(self, maxl=0, nodes=0):
        self.maxl = maxl
        self.nodes = nodes

    def __repr__(self):
        return ("Info[Max Length: {}, Nodes processed: {}]"
                .format(self.maxl, self.nodes))


def reconstruct_path(node):
    pc = []
    cur = node
    while cur:
        pc.append(cur.content)
        cur = cur.parent
    pc.reverse()
    return pc


def a_star(start, goal, h, gen_children):
    L = [Node(start, None, value=h(start), depth=0)]
    visited = set()
    info = Info()

    while L:
        info.maxl = max(len(L), info.maxl)
        info.nodes += 1

        node = hq.heappop(L)
        visited.add(node.content)

        if goal(node.content):
            pc = reconstruct_path(node)
            return pc, info

        for child in gen_children(node.content):
            if child in visited:
                continue
            else:
                parent = node
                depth = node.depth + 1
                f = h(child) + depth
                hq.heappush(L, Node(child, parent, f, depth))

    return None, info


def generic_search(start, is_goal, gen_children,
                   L, get_func, put_func):
    put_func(L, Node(start))
    info = Info()
    visited = set()

    while L:
        info.maxl = max(len(L), info.maxl)
        info.nodes += 1

        current = get_func(L)

        if is_goal(current.content):
            pc = reconstruct_path(current)
            return pc, info

        visited.add(current.content)

        for child in gen_children(current.content):
            if child in visited:
                continue
            x = Node(child, current)
            x.depth = current.depth + 1
            put_func(L, x)

    return None, info


class Reversed:
    def __init__(self, gen):
        self.gen = gen

    def __call__(self, *a, **kw):
        for el in reversed(list(self.gen(*a, **kw))):
            yield el


class Randomized:
    def __init__(self, gen):
        self.gen = gen

    def __call__(self, *a, **kw):
        children = list(self.gen(*a, **kw))
        shuffle(children)
        yield from children


def depth_first(start, is_goal, gen_children):
    return generic_search(start, is_goal, gen_children,
                          deque(), deque.popleft, deque.appendleft)


def breadth_first(start, is_goal, gen_children):
    return generic_search(start, is_goal, gen_children,
                          deque(), deque.pop, deque.appendleft)


class NeighborsGenerator:
    def __init__(self, matrix, w, h):
        self.matrix = matrix
        self.w = w
        self.h = h

    def _canMoveUp(self, x, y):
        return y > 0 and self.matrix[x, y - 1] == 1

    def _canMoveDown(self, x, y):
        return y < self.h - 1 and self.matrix[x, y + 1] == 1

    def _canMoveLeft(self, x, y):
        return x > 0 and self.matrix[x - 1, y] == 1

    def _canMoveRight(self, x, y):
        return x < self.w - 1 and self.matrix[x + 1, y] == 1

    def __call__(self, n):
        x, y = n
        if self._canMoveUp(x, y):
            yield (x, y - 1)
        if self._canMoveLeft(x, y):
            yield (x - 1, y)
        if self._canMoveDown(x, y):
            yield (x, y + 1)
        if self._canMoveRight(x, y):
            yield (x + 1, y)


def print_sol(matrix, sol, msg):
    sol_len = len(sol)
    sol = set(sol)
    r, c = matrix.shape
    print(msg, " [length={}]".format(sol_len))
    for i in range(r):
        for j in range(c):
            if (i, j) in sol:
                print("O", end="")
            elif matrix[i, j] == 1:
                print(" ", end="")
            else:
                print(".", end="")
        print()
    print()


if __name__ == "__main__":
    matrix = np.random.randint(0, 3, (50, 100))
    matrix = np.sign(matrix)
    r, c = matrix.shape
    matrix[0, 0] = matrix[r - 1, c - 1] = 1
    print(matrix)

    child_gen = NeighborsGenerator(matrix, r, c)
    goal_pred = lambda t: t == (r - 1, c - 1)
    heuristic = lambda t: r + c - t[0] - t[1]
    start = (0, 0)

    solution = depth_first(start, goal_pred, child_gen)[0] or []
    print_sol(matrix, solution, "DF")
    # solution = breadth_first(start, goal_pred, child_gen)[0] or []
    # print_sol(matrix, solution, "BF")
    solution = a_star(start, goal_pred, heuristic, child_gen)[0] or []
    print_sol(matrix, solution, "A*")

