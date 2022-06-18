from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class View:
    def __init__(self):
        self.view_loc = Vector3([0.0,4.0, 3.0])
        self.front_view = Vector3([0.0, 0.0, -1.0])
        self.top_view = Vector3([0.0, 1.0, 0.0])
        self.right_view = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.3
        self.val = -90
        self.values = 0

    def current_location_view(self):
        return matrix44.create_look_at(self.view_loc, self.view_loc + self.front_view, self.top_view)

    def calculating_new_location(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.val += xoffset
        self.values += yoffset

        if constrain_pitch:
            if self.values > 45:
                self.values = 45
            if self.values < -45:
                self.values = -45

        self.update_view_position()

    def update_view_position(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.val)) * cos(radians(self.values))
        front.y = sin(radians(self.values))
        front.z = sin(radians(self.val)) * cos(radians(self.values))

        self.front_view = vector.normalise(front)
        self.right_view = vector.normalise(vector3.cross(self.front_view, Vector3([0.0, 1.0, 0.0])))
        self.top_view = vector.normalise(vector3.cross(self.right_view, self.front_view))

    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.view_loc += self.front_view * velocity
        if direction == "BACKWARD":
            self.view_loc -= self.front_view * velocity
        if direction == "LEFT":
            self.view_loc -= self.right_view * velocity
        if direction == "RIGHT":
            self.view_loc += self.right_view * velocity