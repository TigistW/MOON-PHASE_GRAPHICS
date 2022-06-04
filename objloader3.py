import os
import pygame
from OpenGL.GL import *

path = ''
class OBJ:
    generate_on_init = True

    @classmethod
    def loadTexture(cls, imagefile):
        return texid

    @classmethod
    def loadMaterial(cls, filename):
        return contents

    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        dirname = os.path.dirname(filename)
    def render(self):
        glCallList(self.gl_list)

    def free(self):
        glDeleteLists([self.gl_list])
