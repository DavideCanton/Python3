__author__ = 'davide'

import numpy as np
import pygame
from pygame import draw, gfxdraw
from pygame.constants import *
from pygame.color import THECOLORS

W, H = 800, 600
CENTER = 200, H // 2
C_W = 5

def drawCircle(surf, center, radius):
    gfxdraw.filled_circle(surf, center[0], center[1], radius, THECOLORS["blue"])
    gfxdraw.filled_circle(surf, center[0], center[1], radius - C_W, THECOLORS["white"])

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((W, H))

    bgcolor = THECOLORS["white"]
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bgcolor)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
            elif (event.type == KEYDOWN and
                  event.key == K_F4 and
                  event.mod & KMOD_ALT):
                exit()
            elif (event.type == KEYDOWN and
                  event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT)):
                if event.key == K_UP:
                    bar.incr_angle()
                elif event.key == K_DOWN:
                    bar.decr_angle()
                elif event.key == K_LEFT:
                    src.incr_angle()
                elif event.key == K_RIGHT:
                    src.decr_angle()

        background.fill(bgcolor)
        screen.blit(background, (0, 0))
        drawCircle(screen, CENTER, 100)
        pygame.display.flip()