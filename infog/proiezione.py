from pygame.locals import *
from pygame import display, event, draw
import pygame

width = 400
height = 300


class scale(object):
    def __init__(self, nx=0, ny=0, multx=1, multy=1):
        self.nx = nx
        self.ny = ny
        self.multx = multx
        self.multy = multy

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            x, y = func(*args, **kwargs)
            return (x + self.nx) * self.multx, (y + self.ny) * self.multy
        return wrapper


def getLines():
    a = [0, -50, 1]
    b = [0, 50, 1]
    c = [50, 50, 0.5]
    d = [50, -50, 0.5]
    e = [-50, 50, 0.5]
    f = [-50, -50, 0.5]
    return [(a, b), (a, d), (b, c), (a, f), (b, e), (e, f), (c, d)]


@scale(nx=1000, ny=200, multx=0.5, multy=0.5)
def processPoint(x, y, z, d=1):
    if abs(z) > 1E-14:
        return d * x / z, d * y / z
    else:
        return x, y


if __name__ == '__main__':

    display.init()
    screen = display.set_mode((width, height), pygame.RESIZABLE)
    screen.fill(color.Color("white"))
    d = 1

    lines = [(processPoint(*line[0], d=d), processPoint(*line[1], d=d))
             for line in getLines()]

    for line in lines:
        print(line)

    while True:
        for e in event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_F4 and e.mod & KMOD_ALT:
                    exit()
            # handle video resizing
            elif e.type == VIDEORESIZE:
                screen = display.set_mode(e.size, pygame.RESIZABLE)
                screen.fill(color.Color("white"))

        for line in lines:
            draw.line(screen, color.Color("black"), line[0], line[1], 1)
        display.flip()
