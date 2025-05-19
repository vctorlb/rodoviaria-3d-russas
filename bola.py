import numpy as np
from OpenGL.GL import *

def bola(raio, lados, pilhas):
    for i in range(pilhas):
        lat0 = np.pi * (-0.5 + i / pilhas)
        lat1 = np.pi * (-0.5 + (i + 1) / pilhas)
        z0, zr0 = raio * np.sin(lat0), raio * np.cos(lat0)
        z1, zr1 = raio * np.sin(lat1), raio * np.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(lados + 1):
            v = ((i // 5) + (j // 5)) % 2
            glColor3f(v, v, v)

            lng = 2 * np.pi * j / lados
            x, y = np.cos(lng), np.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)

            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def draw_ball(pos=(0.0, 0.3, 0.0), raio=0.3):
    glPushMatrix()
    glTranslatef(*pos)
    bola(raio, 50, 50)
    glPopMatrix()
