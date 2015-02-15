import os
import sys
import pygame
from pygame.locals import *

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')
directory = "data"


class NoneSound:
    def play(self):
        pass


def load_image(name, colorkey=None):
    fullname = os.path.join(directory, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        sys.exit(message)
    image = image.convert()
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join(directory, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        sys.exit(message)
    return sound


class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.punching = False

    def update(self):
        """move the fist based on the mouse position"""
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        """returns collide > 0 if the fist collides with the target"""
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            clip = hitbox.clip(target.rect)
            return clip.width

    def unpunch(self):
        """called to pull the fist back"""
        self.punching = False


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image('chimp.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0
        self.hits = 0

    def getHits(self):
        return self.hits

    def update(self):
        """walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if (self.rect.left < self.area.left or
                self.rect.right > self.area.right):
                self.move = -self.move

            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def _spin(self):
        """spin the monkey image"""
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            self.image = pygame.transform.rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image
            self.hits += 1

    def setDiff(self, val):
        sign = -1 if self.move < 0 else 1
        self.move = (9 + val) * sign


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((600, 60))
    pygame.mouse.set_visible(0)

    bgcolor = 250, 250, 250
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(bgcolor)

    font = pygame.font.Font(None, 36)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    chimp = Chimp()
    fist = Fist()
    allsprites = pygame.sprite.Group((fist, chimp))
    clock = pygame.time.Clock()
    going = True
    points = 0
    factor = 10
    loss = 10

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
            elif event.type == MOUSEBUTTONDOWN:
                collide = fist.punch(chimp)
                if collide:
                    punch_sound.play()  # punch
                    chimp.punched()
                    points += collide * factor
                    chimp.setDiff(points / 1000)
                else:
                    whiff_sound.play()  # miss
                    points -= loss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        background.fill(bgcolor)
        text = font.render("Punch the chimp!!! Points: {}"
                           .format(points), 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        pygame.display.set_caption('Monkey Fever [@ {:1.0f} fps]'
        .format(clock.get_fps()))
        background.blit(text, textpos)
        allsprites.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
