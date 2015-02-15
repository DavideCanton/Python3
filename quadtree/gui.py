__author__ = 'davide'

from random import randint
from quadtree import QuadTree, Rect
import pygame
from pygame.constants import *
from pygame.color import THECOLORS
from pygame.draw import rect, circle, line

W = 800
H = 600
R = 2
N = 100


def col(name):
    """
    @type name: str
    @return the color as a tuple
    """
    return THECOLORS[name]


def draw(surf, qt):
    """
    @param surf: the surface
    @type surf: pygame.Surface
    @param qt: quadtree
    @type qt: QuadTree
    """
    for node in qt:
        rb = node.bounds
        rect_ = pygame.Rect(rb.x, rb.y, rb.w, rb.h)
        if node.val:
            circle(surf, col("red"), node.val[0], R)
        rect(surf, col("black"), rect_, 1)


def main():
    pygame.init()

    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    data = [(randint(0, W), randint(0, H)) for _ in range(N)]
    qt = QuadTree([], W, H)
    i = 0
    going = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif (event.type == KEYDOWN
                  and event.key == K_F4
                  and event.mod & KMOD_ALT):
                going = False

        if not going:
            break

        if i < len(data):
            qt.add_node(data[i])
            qt.assert_correct()

        screen.fill(col("white"))
        draw(screen, qt)
        pygame.display.flip()

        clock.tick(10)
        i += 1


if __name__ == "__main__":
    main()