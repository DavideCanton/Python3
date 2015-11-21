from pygame.time import Clock
from pygame.display import *
from pygame.event import get as get_event
from pygame.constants import *
from pygame.draw import circle, line
from pygame.color import THECOLORS
from datetime import datetime
from math import cos, sin, radians
from os import environ

__author__ = 'davide'
W = 400
RADIUS = W // 2
CENTER = RADIUS, RADIUS

if __name__ == "__main__":
    environ['SDL_VIDEO_CENTERED'] = '1'
    init()
    screen = set_mode((W, W))
    clock = Clock()
    n = datetime.now()
    sangle = -90 + 6 * n.second

    while True:
        clock.tick(24)

        for e in get_event():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_F4 and e.mod & KMOD_ALT:
                    exit()

        rsa = radians(sangle)
        dest = RADIUS + RADIUS * cos(rsa), RADIUS + RADIUS * sin(rsa)

        screen.fill(THECOLORS["white"])

        circle(screen, THECOLORS["black"], CENTER, RADIUS, 3)

        # secondi
        line(screen, THECOLORS["black"], CENTER, dest)
        sangle = (sangle + .25) % 360

        # minuti
        mangle = radians(-90 + 6 * n.minute)
        mdest = RADIUS + RADIUS * cos(mangle), RADIUS + RADIUS * sin(mangle)
        line(screen, THECOLORS["black"], CENTER, mdest, 4)

        # ore
        hangle = radians(-90 + 30 * n.hour)
        hdest = RADIUS + RADIUS // 2 * cos(hangle), RADIUS + RADIUS // 2 * sin(
            hangle)
        line(screen, THECOLORS["black"], CENTER, hdest, 4)

        n = datetime.now()
        set_caption("{:>02}:{:>02}:{:>02}".format(n.hour, n.minute, n.second))
        flip()
