import numpy as np
from OpenGL.GL import *

def _draw_sphere(radius, slices, stacks):
    for i in range(stacks):
        lat0 = np.pi * (-0.5 + i / stacks)
        lat1 = np.pi * (-0.5 + (i + 1) / stacks)
        z0, zr0 = radius * np.sin(lat0), radius * np.cos(lat0)
        z1, zr1 = radius * np.sin(lat1), radius * np.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            v = ((i // 5) + (j // 5)) % 2
            glColor3f(v, v, v)

            lng = 2 * np.pi * j / slices
            x, y = np.cos(lng), np.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)

            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def draw_ball(pos=(0.0, 0.3, 0.0), radius=0.3):
    glPushMatrix()
    glTranslatef(*pos)
    _draw_sphere(radius, 50, 50)
    glPopMatrix()
