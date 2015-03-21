__author__ = 'davide'

from pygame.constants import *
import pygame
import os

BLACK = 0, 0, 0

def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        sys._exit(message)
    image = image.convert_alpha()
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


class PacMan(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = img.get_rect()
        self.speed = [1, 0]

    def update(self, *args):
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]

    def up(self):
        self.speed = [0, -1]

    def down(self):
        self.speed = [0, 1]

    def left(self):
        self.speed = [-1, 0]

    def right(self):
        self.speed = [1, 0]


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((600, 600))
    pygame.mouse.set_visible(0)

    bgcolor = BLACK
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bgcolor)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    pacman = PacMan(load_image("pacman.png"))
    allsprites = pygame.sprite.Group([pacman])

    clock = pygame.time.Clock()
    going = True

    while going:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif (event.type == KEYDOWN and
                  event.key == K_F4 and
                  event.mod & KMOD_ALT):
                going = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    pacman.up()
                if event.key == K_DOWN:
                    pacman.down()
                if event.key == K_LEFT:
                    pacman.left()
                if event.key == K_RIGHT:
                    pacman.right()

        background.fill(bgcolor)
        pygame.display.set_caption('PacMan')
        allsprites.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
