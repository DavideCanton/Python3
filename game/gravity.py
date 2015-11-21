__author__ = 'davide'

from math import sin, cos, pi
import numpy as np
import pygame
from pygame import *
from pygame.color import THECOLORS

W, H = 800, 600
R1 = 5
R2 = 50
M1_POS = 0, H
M1_VEL = 10 * np.array([cos(pi / 2), -sin(pi / 2)])
M1_DENSITY = 1
M2_POS = 400, 300
M2_VEL = 0, 0
M2_DENSITY = 1e9
G = 6.674 * 1e-11

class Mass:
    def __init__(self, radius, position, velocity, density, color, masses):
        self.radius = radius
        self.position = np.array(position, dtype=np.float)
        self.mass = density * (4 / 3 * pi * (radius / 20) ** 3)
        self.masses = masses
        self.velocity0 = np.array(velocity, dtype=np.float)
        self.position0 = np.array(position, dtype=np.float)
        self.color = color

    def update(self, t):
        force = np.zeros((2,))
        for m in self.masses:
            if m == self:
                continue
            r = (m.position - self.position) / 20
            norm_r = np.linalg.norm(r)
            if norm_r >= R2 / 20:
                force += G * m.mass * self.mass / (norm_r ** 3) * r

        acc = 20 * force / self.mass
        self.position = self.position0 + self.velocity0 * t + acc / 2 * t * t

    def draw(self, screen):
        pygame.draw.circle(screen, THECOLORS[self.color],
                           np.array(self.position, dtype=np.int32),
                           self.radius)

def toClose(event):
    return (event.type == QUIT or
            event.type == KEYDOWN and event.key == K_ESCAPE or
            event.type == KEYDOWN and event.key == K_F4 and event.mod & KMOD_ALT)

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((W, H))

    bgcolor = THECOLORS["black"]
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bgcolor)

    masses = []
    m1 = Mass(R1, M1_POS, M1_VEL, M1_DENSITY, "red", masses)
    m2 = Mass(R2, M2_POS, M2_VEL, M2_DENSITY, "yellow", masses)
    masses.extend([m1, m2])

    screen.blit(background, (0, 0))
    pygame.display.flip()

    t = 0
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60)
        t += dt

        for event in pygame.event.get():
            if toClose(event):
                exit()

        background.fill(bgcolor)
        title = "Gravity"
        pygame.display.set_caption(title)

        for m in masses:
            m.update(t / 1000)

        screen.blit(background, (0, 0))

        for m in masses:
            m.draw(screen)

        pygame.display.flip()
