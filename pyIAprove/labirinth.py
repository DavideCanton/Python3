from PIL import Image
from pyIA2.searching import *
import argparse
from math import sqrt
import os.path as ospath
from collections import namedtuple, defaultdict


func_table = [ida_star, a_star, iterative_broadening,
              iterative_deepening, depth_first, breadth_first]


class NeighboursGenerator:
    def __init__(self, labirinth, w, h):
        self.labirinth = labirinth
        self.w = w
        self.h = h

    def _canMoveUp(self, x, y):
        return y > 0 and self.labirinth[x, y - 1] == 1

    def _canMoveDown(self, x, y):
        return y < self.h - 1 and self.labirinth[x, y + 1] == 1

    def _canMoveLeft(self, x, y):
        return x > 0 and self.labirinth[x - 1, y] == 1

    def _canMoveRight(self, x, y):
        return x < self.w - 1 and self.labirinth[x + 1, y] == 1

    def __call__(self, n):
        x, y = n
        if self._canMoveUp(x, y):
            yield (x, y - 1)
        if self._canMoveDown(x, y):
            yield (x, y + 1)
        if self._canMoveLeft(x, y):
            yield (x - 1, y)
        if self._canMoveRight(x, y):
            yield (x + 1, y)


class NeighboursGeneratorDiag(NeighboursGenerator):
    def __init__(self, labirinth, w, h):
        self.labirinth = labirinth
        self.w = w
        self.h = h

    def __call__(self, n):
        x, y = n
        if self._canMoveUp(x, y) and self._canMoveLeft(x, y):
            yield (x - 1, y - 1), 1
        if self._canMoveUp(x, y) and self._canMoveRight(x, y):
            yield (x + 1, y - 1), 1
        if self._canMoveDown(x, y) and self._canMoveLeft(x, y):
            yield (x - 1, y + 1), 1
        if self._canMoveDown(x, y) and self._canMoveRight(x, y):
            yield (x + 1, y + 1), 1
        if self._canMoveLeft(x, y):
            yield (x - 1, y), 0
        if self._canMoveUp(x, y):
            yield (x, y - 1), 0
        if self._canMoveRight(x, y):
            yield (x + 1, y), 0
        if self._canMoveDown(x, y):
            yield (x, y + 1), 0


def parseArgs():
    handler = argparse.ArgumentParser(description="Labirinth search")

    handler.add_argument('-d', '--heuristic', help="Heuristic",
                         default=1, dest="h")

    handler.add_argument('-f', '--algorithm', help="Algorithm",
                         default=0, dest="f")

    handler.add_argument('-g', '--gen', help="Gen",
                         default=0, dest="g")

    handler.add_argument('-i', '--input', help="File di input",
                         dest="ifile")

    handler.add_argument('-o', '--output', help="File di output",
                         dest="ofile")

    return handler.parse_args()


def a_vs_ida_test(imgn=1):
    lab_path = r"D:\labirinth"
    red = 255, 0, 0
    green = 0, 255, 0
    blue = 0, 0, 255
    ext = "bmp"
    # algs = ("ida", "a", "iterative_broadening",
    #        "iterative_deepening", "depth_first")
    algs = ("ida", "a",)
    parsers = []
    res = []
    Contenitore = namedtuple("Contenitore", "ifile, ofile, h, f, g")

    for i, name in enumerate(algs):
        ifile = ospath.join(lab_path, "lab{}.{}".format(imgn, ext))
        ofile = ospath.join(lab_path, "lab{}_{}_".format(imgn, name))
        p = Contenitore(ifile=ifile, ofile=ofile, h=1, f=i, g=0)
        parsers.append(p)

    for parser in parsers:
        imgpath = parser.ifile
        labirinth = defaultdict(int)
        im = Image.open(imgpath)
        pix = im.load()
        h, w = im.size
        print("Reading labirinth from {}...".format(imgpath))

        if parser.h == 0:
            heuristic = lambda pos: 0
        elif parser.h == 1:
            heuristic = lambda pos: (abs(pos[0] - goal[0]) +
                                     abs(pos[1] - goal[1]))
        elif parser.h == 2:
            heuristic = lambda pos: sqrt((pos[0] - goal[0]) ** 2 +
                                         (pos[1] - goal[1]) ** 2)
        else:
            heuristic = lambda pos: ((abs(pos[0] - goal[0]) +
                                      abs(pos[1] - goal[1]))) / 2

        alg = func_table[parser.f]

        name = alg.__name__.replace("_star", "*").replace("_", " ").upper()
        print("Chosen algorithm: {}".format(name))

        if parser.g == 0:
            gen = NeighboursGenerator(labirinth, w, h)
            print("Chosen moveset: MANHATTAN_ONLY")
        else:
            gen = NeighboursGeneratorDiag(labirinth, w, h)
            print("Chosen moveset: MANHATTAN_WITH_DIAGONALS")

        start = goal = None
        for i in range(w):
            for j in range(h):
                if any(pix[j, i]):
                    labirinth[i, j] = 1
                if pix[j, i][0] > pix[j, i][1]:
                    start = i, j
                elif pix[j, i][0] < pix[j, i][1]:
                    goal = i, j

        print("Start detected:\t{}".format(start))
        print("Goal detected:\t{}".format(goal))
        print("Starting search...")

        goal_predicate = lambda g: g == goal
        if parser.f < 2:
            path, visited, info = alg(start, goal_predicate,
                                      heuristic, gen)
        elif parser.f == 2:
            path, *visited, info = alg(start, goal_predicate,
                                       gen, 4)
        elif parser.f > 2:
            path, *visited, info = alg(start, goal_predicate,
                                       gen)

        print("Search ended")
        print("Nodes searched: {}".format(info.nodes))
        print("Maximum list size: {}".format(info.maxl))
        if path is None:
            print("Path not found")
            exit()
        else:
            print("Found path of {} nodes, writing image...".format(len(path)))

        for (i, j) in visited:
            pix[j, i] = blue
        for (i, j) in path[1:-1]:
            pix[j, i] = red
        pix[start[1], start[0]] = green
        pix[goal[1], goal[0]] = green

        val = len(path)
        im.save(parser.ofile + str(val) + ".bmp")
        res.append(val)
        print("Path generation completed")
        print("*" * 100)

    if not all(x == res[0] for x in res):
        print("ERRORE: {}".format(res))


def main_script():
    red = 255, 0, 0
    blue = 0, 0, 255
    parser = parseArgs()

    imgpath = parser.ifile
    labirinth = defaultdict(int)
    im = Image.open(imgpath)
    pix = im.load()
    h, w = im.size
    print("Reading labirinth from {}...".format(imgpath))

    if parser.h == 0:
        heuristic = lambda pos: 0
    elif parser.h == 1:
        heuristic = lambda pos: (abs(pos[0] - goal[0]) +
                                 abs(pos[1] - goal[1]))
    else:
        heuristic = lambda pos: ((pos[0] - goal[0]) ** 2 +
                                 (pos[1] - goal[1]) ** 2)

    alg = func_table[parser.f]

    name = alg.__name__.replace("_star", "*").replace("_", " ").upper()
    print("Chosen algorithm: {}".format(name))

    if parser.g == 0:
        gen = NeighboursGenerator(labirinth, w, h)
        print("Chosen moveset: MANHATTAN_ONLY")
    else:
        gen = NeighboursGeneratorDiag(labirinth, w, h)
        print("Chosen moveset: MANHATTAN_WITH_DIAGONALS")

    start = goal = None
    for i in range(w):
        for j in range(h):
            if any(pix[j, i]):
                labirinth[i, j] = 1
            if pix[j, i][0] > pix[j, i][1]:
                start = i, j
            elif pix[j, i][0] < pix[j, i][1]:
                goal = i, j

    print("Start detected:\t{}".format(start))
    print("Goal detected:\t{}".format(goal))
    print("Starting search...")

    goal_predicate = lambda g: g == goal
    if parser.f < 2:
        path, visited, info = alg(start, goal_predicate,
                                  heuristic, gen)
    elif parser.f == 2:
        path, *visited, info = alg(start, goal_predicate,
                                   gen, 4)
    elif parser.f > 2:
        path, *visited, info = alg(start, goal_predicate,
                                   gen)

    print("Search ended")
    print("Nodes searched: {}".format(info.nodes))
    print("Maximum list size: {}".format(info.maxl))
    if path is None:
        print("Path not found")
        exit()
    else:
        print("Found path of {} nodes, writing image...".format(len(path)))

    for (i, j) in visited:
        pix[j, i] = blue
    for (i, j) in path:
        pix[j, i] = red

    im.save(parser.ofile + str(len(path)) + ".bmp")
    print("Path generation completed")
    print("*" * 100)


if __name__ == '__main__':
    a_vs_ida_test(4)
