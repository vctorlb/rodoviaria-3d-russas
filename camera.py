import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Camera:
    def __init__(self, width, height):
        self.camera_pos = np.array([0.0, 5.0, 10.0])  # Posição inicial mais elevada
        self.camera_front = np.array([0.0, -0.5, -1.0])  # Ângulo de visão para baixo
        self.camera_up = np.array([0.0, 1.0, 0.0])
        self.yaw, self.pitch = -90.0, -30.0  # Ângulo inicial da câmera

        self.camera_speed = 0.08
        self.keys = {}
        self.first_mouse = True
        self.cursor_disabled = True  # Cursor desativado por padrão
        self.sensitivity = 0.1
        self.last_x, self.last_y = width / 2, height / 2

    def update_camera(self):
        glLoadIdentity()
        camera_target = self.camera_pos + self.camera_front
        gluLookAt(*self.camera_pos, *camera_target, *self.camera_up)

    def key_callback(self, window, key, scancode, action, mods):
        self.keys[key] = action == glfw.PRESS

    def process_input(self, window):
        if self.keys.get(glfw.KEY_W, False):
            self.camera_pos += self.camera_speed * self.camera_front
        if self.keys.get(glfw.KEY_S, False):
            self.camera_pos -= self.camera_speed * self.camera_front
        if self.keys.get(glfw.KEY_A, False):
            self.camera_pos -= np.cross(self.camera_front, self.camera_up) * self.camera_speed
        if self.keys.get(glfw.KEY_D, False):
            self.camera_pos += np.cross(self.camera_front, self.camera_up) * self.camera_speed

    def mouse_callback(self, window, xpos, ypos):
        if self.first_mouse:
            self.last_x, self.last_y = xpos, ypos
            self.first_mouse = False

        xoffset = (xpos - self.last_x) * self.sensitivity
        yoffset = (self.last_y - ypos) * self.sensitivity
        self.last_x, self.last_y = xpos, ypos

        self.yaw += xoffset
        self.pitch = np.clip(self.pitch + yoffset, -89.0, 89.0)

        direction = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.camera_front = direction / np.linalg.norm(direction)