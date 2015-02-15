__author__ = 'davide'

from math import sin, cos, radians, tan, acos, sqrt, degrees, pi
import numpy as np
import pygame
from pygame import draw
from pygame.constants import *
from pygame.color import THECOLORS

W, H = 800, 600
SRC_POINT = 0, 0
DST_POINT = W // 2, H
BAR_LENGTH = 500
BAR_STEP = 5
SRC_STEP = 5


class RotatableObject:
    def __init__(self, start_angle, min_angle, max_angle, step):
        self.angle = start_angle
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.step = step

    def incr_angle(self):
        self.angle = min(self.angle + self.step, self.max_angle)

    def decr_angle(self):
        self.angle = max(self.angle - self.step, self.min_angle)


class Bar(RotatableObject):
    def __init__(self, start_point, length, bar_step):
        super(Bar, self).__init__(90, 0, 180, bar_step)
        self.start = np.array(start_point).astype(float)
        self.length = length

    def draw_bar(self, surf):
        if not self.is_horizontal():
            end_pos = (self.start[0] + self.length * cos(radians(self.angle)),
                       self.start[1] - self.length * sin(radians(self.angle)))
        else:
            end_pos = (self.start[0] + self.length * (90 - self.angle) / 90, self.start[1])
        draw.line(surf, THECOLORS["blue"], self.start, end_pos, 5)

    def is_horizontal(self):
        return self.angle in (0, 180)


class Source(RotatableObject):
    def __init__(self, start_point, bar, src_step):
        super(Source, self).__init__(45, 0, 90, src_step)
        self.start = np.array(start_point).astype(float)
        self.bar = bar

    def draw_src(self, surf):
        normalize = lambda v: v / np.linalg.norm(v)
        tga = tan(radians(self.angle))
        tgo = tan(radians(self.bar.angle))
        intersection = self._computeIntersection(bar, tga, tgo)
        if intersection is not None:
            intI = intersection.astype(int)
            draw.line(surf, THECOLORS["red"], self.start, intI, 5)
            Ri = normalize(np.array([-1, -tga]))
            if not bar.is_horizontal():
                N = normalize(np.array([-1, -1 / tgo]))
            else:
                N = np.array([0, -1])
            Ro = normalize(2 * N * (np.dot(Ri, N)) - Ri)
            Ro *= 1000
            #draw.line(surf, THECOLORS["orange"], intI, intI + N * 100, 5)
            draw.line(surf, THECOLORS["green"], intI, intI + Ro, 5)
        else:
            draw.line(surf, THECOLORS["red"], self.start, (W, W * tga), 5)

    def _computeIntersection(self, bar, tga, tgo):
        x0, y0 = bar.start
        x = (x0 * tgo + y0) / (tga + tgo)
        intersection = np.array([x, tga * x]).round(2)
        if bar.is_horizontal():
            if (bar.angle == 0 and intersection[0] < x0 or
                            bar.angle == 180 and intersection[0] > x0):
                return None
        if (intersection[0] > W or intersection[1] > H or
                    intersection[0] < 0 or intersection[1] < 0):
            return None
        dist = np.linalg.norm(intersection - bar.start)
        return intersection if dist <= bar.length else None


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((W, H))

    bgcolor = THECOLORS["white"]
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bgcolor)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    bar = Bar(DST_POINT, BAR_LENGTH, BAR_STEP)
    src = Source(SRC_POINT, bar, SRC_STEP)

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
        title = "Barra [a = {}, o = {}]"
        pygame.display.set_caption(title.format(src.angle, bar.angle))
        screen.blit(background, (0, 0))
        bar.draw_bar(screen)
        src.draw_src(screen)
        pygame.display.flip()
