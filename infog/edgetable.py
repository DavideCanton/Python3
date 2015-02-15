from collections import namedtuple
from math import ceil, floor
import numpy as np
from PIL import Image
import sys


class Screen:
    def __init__(self, w, h):
        self.screen = np.zeros((h, w))
        self.w, self.h = w, h

    def __getitem__(self, key):
        x, y = key
        return self.screen[y, x]

    def __setitem__(self, key, val):
        x, y = key
        self.screen[y, x] = val

    def __str__(self):
        table = list(map(str, reversed(self.screen)))
        number = lambda i: str(len(table) - 1 - i)
        row_gen = (number(i) + "\t" + row for i, row in enumerate(table))
        table = "\n".join(row_gen)
        table += "\n\n \t" + " ".join("{:2d}".format(n)
            for n in range(self.h - 1))
        return table


Point = namedtuple("Point", "x y")


class Edge(namedtuple("Edge_", "p1 p2")):
    @property
    def m(self):
        if self.vertical:
            return sys.maxsize
        return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    @property
    def mInv(self):
        if self.horizontal:
            return 0
        return (self.p2.x - self.p1.x) / (self.p2.y - self.p1.y)

    @property
    def horizontal(self):
        return self.p1.y == self.p2.y

    @property
    def vertical(self):
        return self.p1.x == self.p2.x

    @property
    def pYMin(self):
        return self.p1 if self.p1.y <= self.p2.y else self.p2

    @property
    def pYMax(self):
        return self.p1 if self.p1.y > self.p2.y else self.p2


Bucket = namedtuple("Bucket", "ymax xmin minv")


def makeEdgeTable(screen, edgeList):
    et = [[] for _ in range(screen.h)]
    keyf = lambda e: min(e.p1.y, e.p2.y)
    edgeList = [e for e in sorted(edgeList, key=keyf)
                if not e.horizontal]
    it_edge = iter(edgeList)
    current = next(it_edge)
    try:
        for i in range(screen.h):
            while current.pYMin.y == i:
                ymax = current.pYMax.y
                xmin = current.pYMin.x
                minv = current.mInv
                et[i].append(Bucket(ymax, xmin, minv))
                current = next(it_edge)
    except StopIteration:
        pass
    return et


def paint(screen, edgeList):
    et = makeEdgeTable(screen, edgeList)
    aet = []
    key_func = lambda x: x.xmin
    for i in range(screen.h):
        if not aet and not any(et):
            break
        aet.extend(et[i])
        et[i] = None
        aet = [e for e in sorted(aet, key=key_func) if e.ymax != i]
        parity = False
        for e1, e2 in zip(aet, aet[1:]):
            if not parity:
                for j in range(ceil(e1.xmin), floor(e2.xmin) + 1):
                    screen[j, i] = 1
            parity = not parity
        aet = [Bucket._replace(e, xmin=e.xmin + e.minv) for e in aet]

if __name__ == '__main__':
    w, h = 150, 160
    A, B, C, D, E, F = (Point(20, 30), Point(70, 10), Point(130, 50), Point(130, 130),
                        Point(80, 90), Point(20, 120))
    e = [Edge(A, B), Edge(B, C), Edge(A, F),
         Edge(C, D), Edge(E, F), Edge(E, D)]
    screen = Screen(w, h)
    paint(screen, e)
    im = Image.new("L", (w, h), 255)
    pix = im.load()
    for i in range(w):
        for j in range(h):
            pix[i, h - 1 - j] = (1 - screen[i, j]) * 255
    im.show()
