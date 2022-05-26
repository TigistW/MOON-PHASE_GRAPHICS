import sys
import OpenGL

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from OpenGL.arrays import vbo
import pygame
# import Image
import numpy    

class AClass:
    def __init__(self):
        self.Splash = True    #There's actually more here, but it's impertinent
    def TexFromPNG(self, filename):
        img = Image.open(filename) # .jpg, .bmp, etc. also work
        img_data = numpy.array(list(img.getdata()), 'B')
        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        return texture
    def MakeBuffer(self, target, data, size):
        TempBuffer = glGenBuffers(1)
        glBindBuffer(target, TempBuffer)
        glBufferData(target, size, data, GL_STATIC_DRAW)
        return TempBuffer
    def ReadFile(self, filename):
        tempfile = open(filename,'r')
        source = tempfile.read()
        temprfile.close()
        return source
    def run(self):
        glutInitDisplayMode(GLUT_RGBA)

        glutInitWindowSize(256,244)
        self.window = glutCreateWindow("test")
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.keypress)

        self.MainTex = glGenTextures(1)
        self.SplashTex = self.TexFromPNG("Resources/Splash.png")
        MainVertexData = numpy.array([-1,-1,1,-1,-1,1,1,1],numpy.float32)
        FullWindowVertices = numpy.array([0,1,2,3],numpy.ushort)
        self.MainVertexData = self.MakeBuffer(GL_ARRAY_BUFFER,MainVertexData,len(MainVertexData))
        self.FullWindowVertices = self.MakeBuffer(GL_ELEMENT_ARRAY_BUFFER,FullWindowVertices,len(FullWindowVertices))
        self.BaseProgram = compileProgram(compileShader(self.ReadFile("Shaders/Mainv.glsl"),
                                         GL_VERTEX_SHADER),
                                         compileShader(self.ReadFile("Shaders/Mainf.glsl"),
                                         GL_FRAGMENT_SHADER))
        glutMainLoop()
    def reshape(self, width, height):
        self.width = width
        self.height = height
        glutPostRedisplay()
    def draw(self):
        glViewport(0, 0, self.width, self.height)        

        glClearDepth(1)
        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        if self.Splash:
            glUseProgram(self.BaseProgram)
            pos = glGetAttribLocation(self.BaseProgram, "position")
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.SplashTex)
            glUniform1i(glGetUniformLocation(self.BaseProgram,"texture"), 0)

            glBindBuffer(GL_ARRAY_BUFFER,self.MainVertexData)
            glVertexAttribPointer(pos,
                                  2,
                                  GL_FLOAT,
                                  GL_FALSE,
                                  0,
                                  numpy.array([0],numpy.uint8))
            glEnableVertexAttribArray(pos)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.FullWindowVertices)
            glDrawElements(GL_TRIANGLE_STRIP,
                           4,
                           GL_UNSIGNED_SHORT,
                           numpy.array([0],numpy.uint8))
            glDisableVertexAttribArray(pos)
        else:
            glBindTexture(GL_TEXTURE_2D, self.MainTex)



        glutSwapBuffers()
glutInit(sys.argv)
test = AClass()
test.run()