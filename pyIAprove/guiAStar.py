from tkinter.messagebox import showerror
from pyIA2.searching import *
from pyIAprove.labirinth import *
from collections import defaultdict
from PIL import Image
from tkinter.tix import Tk
from tkinter.ttk import Button, Label, Entry
from math import copysign, exp
from PIL import ImageTk
import time
import threading
import os
from random import randint


SCALE = 5
TIME = 0
NAME = "lab4.bmp"
rt3 = lambda x: x ** (1. / 3.)
p_norm = lambda p, goal: lambda x: (abs(x[0] - goal[0]) ** p +
                                    abs(x[1] - goal[1]) ** p) ** (1.0 / p)
inf_norm = lambda goal: lambda x: max(abs(x[0] - goal[0]),
                                      abs(x[1] - goal[1]))


def wall_weight(goal, labirinth, weight=2):
    def h(pos):
        v1 = v2 = 0
        p = list(pos)
        d = [goal[i] - pos[i] for i in (0, 1)]
        s = [0 if d[i] == 0 else copysign(1, d[i]) for i in (0, 1)]
        while p[0] != goal[0]:
            v1 += (weight - 1) * labirinth[p[0], p[1]] + 1
            p[0] += s[0]
        while p[1] != goal[1]:
            v1 += (weight - 1) * labirinth[p[0], p[1]] + 1
            p[1] += s[1]
        p = list(pos)
        while p[1] != goal[1]:
            v2 += (weight - 1) * labirinth[p[0], p[1]] + 1
            p[1] += s[1]
        while p[0] != goal[0]:
            v2 += (weight - 1) * labirinth[p[0], p[1]] + 1
            p[0] += s[0]
        return min(v1, v2)

    return h


class GUI(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.HMAX = -1
        b1 = Button(self, text="Start A*", command=self.startA)
        b1.grid(row=0, column=0)
        b2 = Button(self, text="Start IDA*", command=self.startIDA)
        b2.grid(row=0, column=1)
        b3 = Button(self, text="Start BF", command=self.startBF)
        b3.grid(row=0, column=2)
        b4 = Button(self, text="Start HC", command=self.startHC)
        b4.grid(row=0, column=3)
        b5 = Button(self, text="Start SA", command=self.startSA)
        b5.grid(row=0, column=4)
        Label(self, text="Heuristic:").grid(row=1, column=0)
        self.hEntry = Entry(self)
        self.hEntry.grid(row=1, column=1, columnspan=4)
        self.initImage()
        self.heur = None

    def initImage(self):
        imgpath = os.path.join(r"D:\labirinth", NAME)
        self.im = Image.open(imgpath)
        self.pix = self.im.load()
        self.h, self.w = self.im.size
        print("Reading labirinth from {}...".format(imgpath))

    def setImage(self, im):
        im2 = im.resize(self.newsize, Image.NEAREST)
        self.image = ImageTk.PhotoImage(im2)
        self.panel.configure(image=self.image)

    def cb(self, L, path=None, reset=False):
        if path is None:
            path = []
        try:
            if L is None:
                L = []
            if reset:
                self.im2 = self.im.copy()
                self.pix2 = self.im2.load()
            for n in L:
                try:
                    _, _, (i, j) = n
                except TypeError:
                    i, j = n.content
                h = self.heur((i, j))
                x = h / self.HMAX
                self.pix2[j, i] = int(x * 255), int((1 - x) * 255), 0
            for n in path:
                i, j = n
                self.pix2[j, i] = 0, 0, 255
            self.pix2[self.start[1], self.start[0]] = 255, 0, 0
            self.setImage(self.im2)
            if TIME:
                time.sleep(TIME)
        except Exception:
            raise
            exit()

    def startA(self):
        self._start("A")

    def startIDA(self):
        self._start("IDA")

    def startBF(self):
        self._start("BF")

    def startHC(self):
        self._start("HC")

    def startSA(self):
        self._start("SA")

    def _start(self, alg):
        self.he = int(self.hEntry.get())
        l = list(self.children.values())
        for ch in l:
            ch.destroy()
        self.alg = alg
        self.panel = Label(self)
        self.panel.pack()
        self.newsize = tuple([int(i * SCALE) for i in self.im.size])
        self.geometry("{}x{}+200+200".format(*self.newsize))
        self.update()
        threading.Thread(target=self.compute).start()

    def get_heuristic(self, start):
        if self.he == 0:
            heuristic = lambda pos: 0
        elif self.he > 1000:
            heuristic = inf_norm(self.goal)
        elif self.he < 0:
            heuristic = wall_weight(self.goal, self.labirinth, -self.he)
        else:
            heuristic = p_norm(self.he, self.goal)

        self.HMAX = max(.1, heuristic(start))
        self.heur = heuristic
        return heuristic

    def compute(self):
        self.labirinth = defaultdict(int)

        gen = NeighboursGenerator(self.labirinth, self.w, self.h)

        self.start = self.goal = None
        for i in range(self.w):
            for j in range(self.h):
                if any(self.pix[j, i]):
                    self.labirinth[i, j] = 1
                if self.pix[j, i][0] > self.pix[j, i][1]:
                    self.start = i, j
                elif self.pix[j, i][0] < self.pix[j, i][1]:
                    self.goal = i, j

        if not self.start or not self.goal:
            raise ValueError("Start or goal not found")

        self.im2 = self.im.copy()
        self.pix2 = self.im2.load()

        print("Start detected:\t{}".format(self.start))
        print("Goal detected:\t{}".format(self.goal))
        print("Starting search...")

        goal_predicate = lambda g: g == self.goal
        heuristic = self.get_heuristic(self.start)
        if self.alg == "IDA":
            alg = ida_star
        elif self.alg == "A":
            alg = a_star
        elif self.alg == "BF":
            alg = best_first
        elif self.alg == "HC":
            alg = hill_climbing
        elif self.alg == "SA":
            alg = simulated_annealing
        else:
            alg = None

        if alg is not None:
            if self.alg == "SA":
                sch = lambda t: exp(-t / 10000)
                path, *_, info = alg(self.start, goal_predicate, heuristic,
                                     gen, sch, self.cb)
            elif self.alg == "A":
                path, *_, info = alg(self.start, goal_predicate, heuristic,
                                     gen, lambda x, y: 1, self.cb)
            else:
                path, *_, info = alg(self.start, goal_predicate, heuristic,
                                     gen, self.cb)

            print("Search ended")
            print("Nodes searched: {}".format(info.nodes))
            print("Maximum list size: {}".format(info.maxl))
            if path is None:
                print("Path not found")
                showerror("Error", "Path not found!")
            else:
                print("Found path of {} nodes".format(len(path)))
                print("Path generation completed")
                print("*" * 100)
                self.cb(None, path)


if __name__ == '__main__':
    GUI().mainloop()
