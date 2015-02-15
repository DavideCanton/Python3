from pygame import *
from pygame.locals import *
from OpenGL.GL import *


class GLHandler:
    def __init__(self, l=.5):
        self.l = l
        self.x = 0
        self.y = 0
        self.x_axis = True


    def initGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)


    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_QUADS)

        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(self.l, 0.0)

        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(0.0, self.l)

        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(-self.l, 0.0)

        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(0.0, -self.l)

        glEnd()

        if self.x_axis:
            self.x += 1
            if self.x > 180:
                self.x = 0
                self.x_axis = False
            glRotatef(1.0, 1.0, 0.0, 0.0)
        else:
            self.y += 1
            if self.y > 180:
                self.y = 0
                self.x_axis = True
            glRotatef(1.0, 0.0, 1.0, 0.0)

        glFlush()

init()
display.set_mode((640, 480), OPENGL)
display.set_caption("Quad OpenGL")
glh = GLHandler()
glh.initGL()
glh.resizeGL(640, 480)
clock = time.Clock()

while True:
    clock.tick(60)

    for e in event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_F4 and e.mod & KMOD_ALT:
                exit()

    glh.paintGL()
    display.flip()
