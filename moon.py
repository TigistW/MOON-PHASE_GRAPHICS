import glfw
import os
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from OpenGL.GL import shaders
from TextureLoader import load_texture
from camera import Camera
from objloader3 import ObjLoader
from PIL import Image

class Moon:
    def __init__(self) -> None:
        global lastX, lastY
        global first_mouse
        self.cam = Camera()
        WIDTH, HEIGHT = 900, 550
        lastX, lastY = WIDTH / 2, HEIGHT / 2
        first_mouse = True

        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")
        glfw.set_window_pos(window, 100, 100)
        glfw.set_window_size_callback(window, self.window)
        glfw.set_cursor_pos_callback(window, self.mouse_look)
        glfw.set_cursor_enter_callback(window, self.mouse_enter)
        glfw.make_context_current(window)

        # importing indices and buffers
        # could return the indices and the buffers in a different function
        moon_indices, moon_buffer = ObjLoader.load_model("MoonBlender/blendermonn.obj")

        self.vertexContent = self.getFileContents("vertex.shader")
        self.fragmentContent = self.getFileContents("fragment.shader")
        self.vertexShader = shaders.compileShader(self.vertexContent, GL_VERTEX_SHADER)
        self.fragmentShader = shaders.compileShader(self.fragmentContent, GL_FRAGMENT_SHADER)

        self.program = glCreateProgram()
        glAttachShader(self.program, self.vertexShader)
        glAttachShader(self.program, self.fragmentShader)
        glLinkProgram(self.program)

        # VAO and VBO declarations
        self.MoonVao = glGenVertexArrays(1)
        self.MoonVbo = glGenBuffers(1)

        # Moon VAO binding
        glBindVertexArray(self.MoonVao)
        # Chibi Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.MoonVbo)
        glBufferData(GL_ARRAY_BUFFER, moon_buffer.nbytes, moon_buffer, GL_STATIC_DRAW)

        # chibi vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, moon_buffer.itemsize * 8, ctypes.c_void_p(0))

        # chibi textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, moon_buffer.itemsize * 8, ctypes.c_void_p(12))
        
        # chibi normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, moon_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        textures = glGenTextures(1)
        load_texture("MoonBlender/MoonTex.jpg", textures)

        glUseProgram(self.program)
        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
        self.moon_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, 0]))

        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45, 1280 / 720, 0.1, 100)

        self.moon_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        # eye, target, up
        view = pyrr.matrix44.create_look_at(pyrr.Vector3(
            [0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

        self.model_loc = glGetUniformLocation(self.program, "model")
        self.proj_loc = glGetUniformLocation(self.program, "projection")
        self.view_loc = glGetUniformLocation(self.program, "view")

        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)

        while not glfw.window_should_close(window):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
            model = pyrr.matrix44.multiply(rot_y, self.moon_pos)

            # draw the moon
            glBindVertexArray(self.MoonVao)
            glBindTexture(GL_TEXTURE_2D, textures)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)
            glDrawArrays(GL_TRIANGLES, 0, len(moon_indices))
            # glDrawElements(GL_TRIANGLES, len(chibi_indices), GL_UNSIGNED_INT, None)
            glfw.swap_buffers(window)

        glfw.terminate()

    def window(self,window, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)

    def getFileContents(self,filename):
        p = os.path.join(os.getcwd(), "Shaders", filename)
        return open(p, 'r').read()

    def mouse_look(self, window, xpos, ypos):
        if self.first_mouse:
            lastX = xpos
            lastY = ypos
        xoffset = xpos - lastX
        yoffset = lastY - ypos
        lastX = xpos
        lastY = ypos
        self.cam.process_mouse_movement(xoffset, yoffset)

    # the mouse enter callback function
    def mouse_enter(self, window, entered):
        
        if entered:
            self.first_mouse = False
        else:
            self.first_mouse = True

    def Texture(self,directory,texture):
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = Image.open(directory)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width,
                    image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return texture
moon = Moon()