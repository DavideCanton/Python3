from pygame import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *


class GLHandler:
    def __init__(self):
        self.l = .5
        self.x = 0
        self.y = 0
        self.x_axis = True


    def initGL(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glShadeModel(GL_FLAT)
        glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 1.0))
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glutInit()


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
        glMaterial(GL_FRONT, GL_EMISSION, (1.0, 0.0, 0.0))
        glMaterial(GL_BACK, GL_EMISSION, (0.0, 1.0, 0.0))
        glutSolidCube(self.l)

        if self.x_axis:
            self.x += 1
            if self.x > 45:
                self.x = 0
                self.x_axis = False
            else:
                glRotatef(1.0, 1.0, 0.0, 0.0)
        else:
            self.y += 1
            if self.y > 30:
                self.y = 0
                self.x_axis = True
            else:
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
