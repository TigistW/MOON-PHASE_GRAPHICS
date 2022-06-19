import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import pyrr
import os
from objloader3 import model_object_loader
from OpenGL.GL import shaders
from View import View
from OpenGL.GL import *
from PIL import Image

viewCam = View()
width, height = 1150, 680
default_X, default_Y = width / 2, height / 2
left_mov, right_mov, front_mov, back_mov, mouse = False, False, False, False,True

def get_texture(path, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    tex_image = Image.open(path)
    tex_image = tex_image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = tex_image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_image.width,tex_image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture

def keyboard_motion(window, keyboard_key,scancode,action,mode):
    global left_mov, right_mov, front_mov, back_mov
    if keyboard_key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if keyboard_key == glfw.KEY_W and action == glfw.PRESS:
        front_mov = True
    elif keyboard_key == glfw.KEY_W and action == glfw.RELEASE:
        front_mov = False
    if keyboard_key == glfw.KEY_S and action == glfw.PRESS:
        back_mov = True
    elif keyboard_key == glfw.KEY_S and action == glfw.RELEASE:
        back_mov = False
    if keyboard_key == glfw.KEY_A and action == glfw.PRESS:
        left_mov = True
    elif keyboard_key == glfw.KEY_A and action == glfw.RELEASE:
        left_mov = False
    if keyboard_key == glfw.KEY_D and action == glfw.PRESS:
        right_mov = True
    elif keyboard_key == glfw.KEY_D and action == glfw.RELEASE:
        right_mov = False

def keyboard_action_movement():
    if left_mov:
        viewCam.keyboard_director("LEFT", 0.04)
    if right_mov:
        viewCam.keyboard_director("RIGHT", 0.04)
    if front_mov:
        viewCam.keyboard_director("FORWARD", 0.04)
    if back_mov:
        viewCam.keyboard_director("BACKWARD", 0.04)

def mouse_motion(window, x_position, y_position):
    global mouse, default_X, default_Y
    if mouse:
        default_X = x_position
        default_Y = y_position
        mouse = False

    x_distance = x_position - default_X
    y_distance = default_Y - y_position

    default_X = x_position
    default_Y = y_position
    viewCam.calculating_new_location(x_distance, y_distance)

def changing_display(display, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(
        45, width / height, 0.1, 100)
    glUniformMatrix4fv(projection_view_location, 1, GL_FALSE, projection)


def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shader", filename)
    return open(p, 'r').read()

def render():
    view = viewCam.current_location_view()
    glUniformMatrix4fv(view_display_location, 1, GL_FALSE, view)

    rot_y = pyrr.Matrix44.from_y_rotation(0.6 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, default_moon_position)

    glBindVertexArray(MoonVao)
    glBindTexture(GL_TEXTURE_2D, textures)

    glUniformMatrix4fv(moon_model_location, 1, GL_FALSE, model)

    glUniformMatrix4fv(transform_loc, 1, GL_FALSE, rot_y)
    glUniformMatrix4fv(light_loc, 1, GL_FALSE, rot_y)
    glDrawArrays(GL_TRIANGLES, 0, len(moon_indices))

if not glfw.init():
    raise Exception("initialization of glfw failed!")
display = glfw.create_window(width, height, "Moon phases", None, None)

glfw.set_window_pos(display, 50, 50)
glfw.set_window_size_callback(display, changing_display)
glfw.set_cursor_pos_callback(display, mouse_motion)
glfw.set_key_callback(display, keyboard_motion)
glfw.set_input_mode(display, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.make_context_current(display)

moon_indices, moon_buffer = model_object_loader.get_model("MoonBlender/MoonObj.obj")

vertexContent = getFileContents("vertex.vs")
fragmentContent = getFileContents("fragment.fs")
vertexShader = shaders.compileShader(vertexContent, GL_VERTEX_SHADER)
fragmentShader = shaders.compileShader(fragmentContent, GL_FRAGMENT_SHADER)

program = glCreateProgram()
glAttachShader(program, vertexShader)
glAttachShader(program, fragmentShader)
glLinkProgram(program)

MoonVao = glGenVertexArrays(1)
MoonVbo = glGenBuffers(1)

glBindVertexArray(MoonVao)

glBindBuffer(GL_ARRAY_BUFFER, MoonVbo)
glBufferData(GL_ARRAY_BUFFER, moon_buffer.nbytes, moon_buffer, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      moon_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      moon_buffer.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      moon_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

textures = glGenTextures(1)
get_texture("MoonBlender/moon_texture.jpg", textures)

glUseProgram(program)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(
    45, 1280 / 720, 0.1, 100)
default_moon_position = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([0, 4, 0]))

moon_model_location = glGetUniformLocation(program, "moon_model")
projection_view_location = glGetUniformLocation(program, "projection_view")
view_display_location = glGetUniformLocation(program, "view_display")
transform_loc = glGetUniformLocation(program, "transform")
light_loc = glGetUniformLocation(program, "light")
glUniformMatrix4fv(projection_view_location, 1, GL_FALSE, projection)

while not glfw.window_should_close(display):
    glfw.poll_events()
    keyboard_action_movement()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    render()
    glfw.swap_buffers(display)

glfw.terminate()