import sys
import pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader3 import *

pygame.init()
viewport = (1280, 720)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | pygame.RESIZABLE)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)

global specref
specref = (1.0, 1.0, 1.0, 1.0)

glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
glMateriali(GL_FRONT, GL_SHININESS, 128)
glShadeModel(GL_SMOOTH)

objMoon = OBJ('Moon 2K.obj', swapyz=False)
objMoon.generate()

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)

glMatrixMode(GL_MODELVIEW)

rx, ry = (0, 0)
tx, ty = (0, 0)
zpos = 5
ypos = 5

rotate = move = False
running = True
while running:
    clock.tick(30)
    keys = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    lightPos = (-50.0, 50.0, 100.0, 1.0)
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    objMoon.render()
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    pygame.display.flip()
pygame.quit()
