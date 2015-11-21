import heapq as hq
from collections import deque
from math import exp
from random import random, choice
from utils import compare_on

__all__ = ["Info", "a_star", "best_first", "breadth_first", "depth_first",
           "generic_search", "hill_climbing", "ida_star",
           "iterative_broadening", "iterative_deepening", "simulated_annealing"]

# infinite represented by -1
INF = -1


@compare_on("value")
class Node:
    def __init__(self, content, parent=None, value=0, depth=0):
        self.content = content
        self.value = value
        self.depth = depth
        self.parent = parent

    def __repr__(self):
        return ("<Node, cnt: {}, val: {}, dpt: {}>"
                .format(self.content, self.value, self.depth))


class Info:
    def __init__(self, curl=0, maxl=0, nodes=0, maxdepth=0):
        self.curl = curl
        self.maxl = maxl
        self.nodes = nodes
        self.maxdepth = maxdepth

    def __repr__(self):
        return (
        "Info[Cur Length: {}, Max Length: {}, Nodes processed: {}, Max depth: "
        "{}]"
        .format(self.curl, self.maxl, self.nodes, self.maxdepth))


def simulated_annealing(start, goal, h, gen_children, schedule, callback=None):
    best = None
    n = Node(start)
    n.value = h(start)
    L = [n]
    info = Info()
    visited = set()
    t = 0
    current = n

    while True:
        if callback:
            callback(L)

        if best is None or current.value > best.value:
            best = current

        T = schedule(t)
        t += 1

        info.maxl = max(len(L), info.maxl)
        info.nodes += 1

        if abs(T) < 1E-10 or goal(current.content):
            n = current
            pc = []
            while n:
                pc.append(n.content)
                n = n.parent
            pc.reverse()
            return pc, None, info

        sons = list(gen_children(current.content))
        nc = choice(sons)
        # while nc in visited:
        #    nc = choice(sons)
        nextNode = Node(nc)
        nextNode.value = h(nc)
        nextNode.depth = current.depth + 1
        nextNode.parent = current
        delta = float(current.value - nextNode.value)
        if delta > 0 or random() < exp(delta / T):
            visited.add(current.content)
            current = nextNode
            L.append(nextNode)
        elif delta < 0 and random() < 0.7:
            current = best
            t = 0

    return None, None, info


def a_star(start, goal, h, gen_children, callback=None, limit=None):
    g = {start: 0}
    c_from = {}
    L = [(h(start), 0, start)]

    visited = set()
    info = Info()
    j = 0

    while L:
        if callback:
            callback(L)

        info.curl = len(L)
        info.maxl = max(info.curl, info.maxl)
        info.nodes += 1

        # if j & 5000 == 0:
        #    print(info)
        j += 1

        _, d, current = hq.heappop(L)
        info.maxdepth = max(info.maxdepth, g[current])
        visited.add(current)

        if goal(current):
            n = current
            pc = []
            while n in c_from:
                pc.append(n)
                n = c_from[n]
            pc.reverse()
            return pc, visited, info

        to_append = []
        for i, child in enumerate(gen_children(current, c_from.get(current), d)):
            child, w = child
            tg = g[current] + w
            if limit is not None and tg > limit:
                continue
            if child in visited:
                if tg >= g[child]:
                    continue
            if child not in g or tg < g[child]:
                c_from[child] = current
                g[child] = tg
                vh = h(child)
                f = g[current] + vh
                to_append.append((f, vh + i, child))

        for child in to_append:
            hq.heappush(L, child)

    return None, None, info


def best_first(start, goal, h, gen_children, callback=None):
    c_from = {}
    L = [(h(start), start)]
    visited = set()
    info = Info()

    while L:
        if callback:
            callback(L)

        info.maxl = max(len(L), info.maxl)
        info.nodes += 1

        _, current = hq.heappop(L)
        visited.add(current)

        if goal(current):
            n = current
            pc = []
            while n in c_from:
                pc.append(n)
                n = c_from[n]
            pc.reverse()
            return pc, visited, info

        for i, child in enumerate(gen_children(current, c_from.get(current))):
            child, w = child
            if child in visited:
                continue
            c_from[child] = current
            vh = h(child)
            hq.heappush(L, (vh, child))

    return None, None, info


def hill_climbing(start, goal, h, gen_children, callback=None):
    c_from = {}
    L = [(h(start), start)]
    visited = set()
    info = Info()

    while L:
        if callback:
            callback(L)

        info.maxl = max(len(L), info.maxl)
        info.nodes += 1

        _, current = hq.heappop(L)
        visited.add(current)

        if goal(current):
            n = current
            pc = []
            while n in c_from:
                pc.append(n)
                n = c_from[n]
            pc.reverse()
            return pc, visited, info

        sons = []
        for i, child in enumerate(gen_children(current, c_from.get(current))):
            child, w = child
            if child in visited:
                continue
            c_from[child] = current
            vh = h(child)
            sons.append((vh, child))
        sons.sort(reverse=True)
        L.extend(sons)

    return None, None, info


def generic_search(start, is_goal, gen_children,
                   L, get_func, put_func, callback=None):
    put_func(L, Node(start))
    info = Info()
    visited = set()

    while L:
        if callback:
            callback(L)

        info.maxl = max(len(L), info.maxl)
        info.nodes += 1

        current = get_func(L)

        if is_goal(current.content):
            n = current
            pc = []
            while n:
                pc.append(n.content)
                n = n.parent
            pc.reverse()
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
        self.vals = list(gen)
        self.vals.reverse()

    def __iter__(self):
        yield from self.vals


def depth_first(start, is_goal, gen_children, left=False, callback=None):
    if left:
        gen_children = Reversed(gen_children)
    return generic_search(start, is_goal, gen_children,
                          deque(), deque.popleft, deque.appendleft, callback)


def breadth_first(start, is_goal, gen_children, callback=None):
    return generic_search(start, is_goal, gen_children,
                          deque(), deque.popleft, deque.append, callback)


def iterative_deepening(start, is_goal, gen_children, callback=None):
    c = 0
    info = Info()

    while True:
        L = [Node(start)]
        visited = set()
        maxdepth = 0

        while L:
            if callback:
                callback(L)

            info.maxl = max(len(L), info.maxl)
            info.nodes += 1

            current = L.pop()
            maxdepth = max(maxdepth, current.depth)

            if is_goal(current.content):
                n = current
                pc = []
                while n:
                    pc.append(n.content)
                    n = n.parent
                pc.reverse()
                return pc, info

            visited.add(current.content)

            if current.depth < c:
                for child in gen_children(current.content):
                    if child in visited:
                        continue
                    x = Node(child, current)
                    x.depth = current.depth + 1
                    L.append(x)

        if maxdepth < c:
            break
        c += 1
        print("Depth:", c)

    return None, info


def iterative_broadening(start, is_goal, gen_children, bmax, callback=None):
    for c in range(1, bmax + 1):
        info = Info()
        print("Branching factor: ", c)
        L = [Node(start)]
        visited = set()
        j = 0

        while L:
            if callback:
                callback(L)

            info.curl = len(L)
            info.maxl = max(info.curl, info.maxl)
            info.nodes += 1

            if j % 5000 == 0:
                print(info)
            j += 1

            current = L.pop()

            info.maxdepth = max(info.maxdepth, current.depth)

            if is_goal(current.content):
                n = current
                pc = []
                while n:
                    pc.append(n.content)
                    n = n.parent
                pc.reverse()
                return pc, info

            visited.add(current.content)

            for i, child in enumerate(gen_children(current.content)):
                if i == c:
                    break
                if child in visited:
                    continue
                x = Node(child, current)
                x.depth = current.depth + 1
                L.append(x)

    return None, info


def ida_star(start, is_goal, h, gen_children, callback=None, limit=None):
    c = 1
    info = Info()
    c_from = {}
    g = {start: 0}

    while True:
        n = h(start), start
        L = [n]
        cp = INF
        visited = {}

        if callback:
            callback(L)

        while L:
            if callback:
                callback(L)
            info.maxl = max(len(L), info.maxl)
            info.nodes += 1

            val, current = L.pop()

            if is_goal(current):
                n = current
                pc = []
                while n in c_from:
                    pc.append(n)
                    n = c_from[n]
                pc.reverse()
                return pc, visited, info

            visited[current] = val

            for child in gen_children(current, c_from.get(current)):
                child, w = child

                if limit is not None and g[current] + w > limit:
                    continue

                g[child] = g[current] + w
                x = h(child) + g[child], child

                if child in visited:
                    if x[0] < visited[child]:
                        visited[child] = x[0]
                    else:
                        continue
                else:
                    visited[child] = x[0]

                if x[0] <= c:
                    L.append(x)
                else:
                    cp = x[0] if cp == INF else min(cp, x[0])

        if cp == INF:
            break

        c = cp
        print("Depth:", c)

    return None, None, info
