from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Lighting:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)

    def setup_day(self):
        glDisable(GL_LIGHTING)

    def setup_night(self):
        glEnable(GL_LIGHTING)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.15, 0.15, 0.2, 1.0])

    def setup_spotlight(self, light_id, position, direction, color, intensity, cutoff, exponent):
        pos_4f = list(position) + [1.0]
        
        glLightfv(light_id, GL_POSITION, pos_4f)
        glLightfv(light_id, GL_SPOT_DIRECTION, direction)
        
        diffuse_color = [c * intensity for c in color] + [1.0]
        glLightfv(light_id, GL_DIFFUSE, diffuse_color)
        glLightfv(light_id, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

        glLightf(light_id, GL_SPOT_CUTOFF, cutoff)
        glLightf(light_id, GL_SPOT_EXPONENT, exponent)
        
        glLightf(light_id, GL_CONSTANT_ATTENUATION, 0.3)
        glLightf(light_id, GL_LINEAR_ATTENUATION, 0.01)
        glLightf(light_id, GL_QUADRATIC_ATTENUATION, 0.005)
        
        glEnable(light_id)

    def draw_spotlight_cone(self, position, direction, cutoff_angle, length=16.0):
        glPushMatrix()
        
        glEnable(GL.GL_BLEND)
        glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)
        glDisable(GL_LIGHTING)

        glColor4f(1.0, 1.0, 0.8, 0.07)

        glTranslatef(position[0], position[1], position[2])

        angle_y = np.degrees(np.arctan2(-direction[0], -direction[2]))
        angle_x = np.degrees(np.arcsin(direction[1]))
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_x, 1, 0, 0)

        quad = gluNewQuadric()
        radius = length * np.tan(np.radians(cutoff_angle))
        gluCylinder(quad, 0.0, radius, length, 16, 1)

        glEnable(GL_LIGHTING)
        glDepthMask(GL_TRUE)
        glDisable(GL.GL_BLEND)

        glPopMatrix()
