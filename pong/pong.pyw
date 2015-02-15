from pygame.locals import *
from pygame import *
from os import path, environ
from random import random
from math import *
from collections import deque


def loadSound(name):
    return mixer.Sound(path.join("data", "sounds", name)) if mixer else None

white = Color("white")
black = Color("black")
red = Color("red")
# size of the screen
width, height = 800, 600
# size of the platform
plat_size = 10, 200
# length subtracted when losing points
plat_decrease = 30
# lower bound to plat length
plat_limit = 100
# points to decrease length
points_to_decrease = 5
# size of the ball
ball_size = 15, 15
# initial speed of the ball
ball_speed = [5, 5]
# movement increase of the ball (2)
movement_increase = 2
# movement speed of the plat
movement = 20
# times to increase ball speed (50)
times_to_increase = 50
# times limit
times_limit = 2000
# initial points
points = [0, 0]
# audio enabled
audio = False
# CPU level [-1 player 0 easy 1 hard]
cpu = [1, 1]
# CPU Memory
cpumem = {}
# length of the tray
traylength = 30


class Platform(object):
    def __init__(self, rect, height):
        self.baserect = rect
        self.rect = self.baserect.copy()
        self.height = height

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.move_ip(0, -movement)

    def moveDown(self):
        if self.rect.bottom < self.height:
            self.rect.move_ip(0, movement)

    def moveTo(self, rect):
        self.rect.centery = rect.centery
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height

    def paint(self, surface):
        s = Surface(self.rect.size)
        s.fill(white)
        surface.blit(s, self.rect)

    def decreaseSize(self, size):
        if self.rect.height - size >= plat_limit:
            self.rect.height -= size

    def reset(self):
        self.rect = self.baserect.copy()


class Ball(object):
    def __init__(self, rect, p1, p2, screenSize, hitSound=None, traylength=0):
        self.rect = rect
        self.p1 = p1
        self.p2 = p2
        self.screenSize = screenSize
        self.hitSound = hitSound
        self.reset()
        self.tray = deque()
        self.traylength = traylength

    def reset(self):
        self.nextCollision = False
        self.times = 0
        self.rect.center = self.screenSize[0] / 2, self.screenSize[1] / 2
        self.speed = ball_speed[:]
        for i in (0, 1):
            if random() >= 0.5:
                self.speed[i] *= -1

    def move(self):
        # decide whether to increase ball speed
        if self.times < times_limit:
            self.times += 1
            if self.times % times_to_increase == 0:
                for i in (0, 1):
                    # increase speed
                    if self.speed[i] >= 0:
                        self.speed[i] += movement_increase
                    else:
                        self.speed[i] -= movement_increase

        pl = None
        if self.nextCollision:
            self.speed[0] *= -1
            if self.hitSound:
                self.hitSound.play()
            self.nextCollision = False
        else:
            # try to move the ball
            urect = self.rect.union(self.rect.move(self.speed))

            # bounce on a platform
            if (self.p1.rect.colliderect(urect) or
                self.p2.rect.colliderect(urect)):
                self.nextCollision = True

            # bounce on an horizontal axe
            if urect.top < 0 or urect.bottom >= self.screenSize[1]:
                self.speed[1] *= -1
            # p2 scored
            elif self.rect.left <= 0:
                pl = self.p2
            # p1 scored
            elif self.rect.right >= self.screenSize[0]:
                pl = self.p1

        r = self.rect.copy()
        r.center = self.rect.center
        r.size = (self.rect.width / 2, self.rect.height / 2)

        self.tray.append(r)
        if len(self.tray) >= self.traylength:
            self.tray.popleft()
        self.rect.move_ip(self.speed)

        return pl

    def paint(self, surface):
        self._paintRect(self.rect, white, surface)
        for r in self.tray:
            self._paintRect(r, red, surface)

    def _paintRect(self, rect, color, surface):
        s = Surface(rect.size)
        s.fill(color)
        surface.blit(s, rect)


def makePlatRect():
    r = rect.Rect((0, 0), plat_size)
    r.centery = height / 2
    return r


def movePlatform(index, platform, ball, keys, cpu, pressed):
    if cpu < 0:
        if pressed[keys[0]]:
            platform.moveUp()
        elif pressed[keys[1]]:
            platform.moveDown()
    elif cpu == 0:
        if random() < .3:
            platform.moveUp()
        elif random() < .3:
            platform.moveDown()
        else:
            platform.moveTo(ball.rect)
    elif cpu > 0:
        platform.moveTo(ball.rect)


if __name__ == '__main__':
    environ['SDL_VIDEO_CENTERED'] = '1'
    init()
    screen = display.set_mode((width, height))
    hit = loadSound("hit.wav") if audio else None
    hurt = loadSound("hurt.wav") if audio else None

    r1 = makePlatRect()
    r1.left = 0
    p1 = Platform(r1, height)
    r2 = makePlatRect()
    r2.right = width
    p2 = Platform(r2, height)
    rb = rect.Rect((0, 0), ball_size)
    b = Ball(rb, p1, p2, (width, height), hit, traylength)
    b.reset()
    players = p1, p2

    myfont = font.Font(None, 100)

    clock = time.Clock()
    paused = False

    while True:
        clock.tick(60)

        if not paused:
            pressed = key.get_pressed()
            movePlatform(0, p1, b, (K_w, K_s), cpu[0], pressed)
            movePlatform(1, p2, b, (K_UP, K_DOWN), cpu[1], pressed)

        for e in event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    paused = not paused
                if e.key == K_F4 and e.mod & KMOD_ALT:
                    exit()

        screen.fill(black)

        if not paused:
            scored = b.move()
            if scored in players:
                index_scored = players.index(scored)
                other_index = 1 - index_scored
                if hurt:
                    hurt.play()
                time.wait(1000)
                b.reset()
                points[index_scored] += 1

                if (points[index_scored] and
                    points[index_scored] % points_to_decrease == 0):
                    players[other_index].decreaseSize(plat_decrease)
        else:
            font_surfacep = myfont.render("Paused", True, white)
            font_rectp = font_surfacep.get_rect(center=(width / 2, height / 2))
            screen.blit(font_surfacep, font_rectp)

        display.set_caption("Pong [running at {} fps]".format(clock.get_fps()))
        font_surface = myfont.render("{}    {}".format(*points), True, white)
        font_rect = font_surface.get_rect(top=0, centerx=width / 2)
        screen.blit(font_surface, font_rect)
        for s in p1, p2, b:
            s.paint(screen)
        display.flip()
