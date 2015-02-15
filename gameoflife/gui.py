__author__ = 'davide'

import pygame
from pygame.constants import *
from pygame.color import THECOLORS
from board import *

W = 16
H = 16


def col(name):
    return THECOLORS[name]


def put_on_surf(p, board):
    for i in range(H):
        for j in range(W):
            p[i, j] = col("black") if board[i, j] else col("white")


def main():
    pygame.init()

    screen = pygame.display.set_mode((600, 600))

    pygame.display.flip()
    clock = pygame.time.Clock()

    going = True
    board = randomBoard(W, H, 0.3)

    pix_array = pygame.PixelArray(pygame.Surface((W, H)))
    put_on_surf(pix_array, board)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif (event.type == KEYDOWN and
                          event.key == K_F4 and
                          event.mod & KMOD_ALT):
                going = False

        if not going:
            break

        pygame.display.set_caption('Life [{} fps]'.format(clock.get_fps()))
        board = advance(board)
        put_on_surf(pix_array, board)
        surface = pix_array.make_surface()
        surface = pygame.transform.scale(surface, (600, 600))
        screen.blit(surface, (0, 0))
        pygame.display.flip()

        clock.tick(100)


if __name__ == "__main__":
    main()