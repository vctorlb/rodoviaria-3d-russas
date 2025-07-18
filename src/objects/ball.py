from OpenGL.GL import *
import numpy as np

class Ball:
    def __init__(self, position, radius=0.22):
        self.position = position
        self.radius = radius

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(90, 1, 0, 0)
        
        stacks = 20
        slices = 20
        
        for i in range(stacks):
            lat0 = np.pi * (-0.5 + i / stacks)
            z0 = self.radius * np.sin(lat0)
            zr0 = self.radius * np.cos(lat0)

            lat1 = np.pi * (-0.5 + (i + 1) / stacks)
            z1 = self.radius * np.sin(lat1)
            zr1 = self.radius * np.cos(lat1)

            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * np.pi * j / slices
                x = np.cos(lng)
                y = np.sin(lng)
                
                color = 1.0 if (i + j) % 2 == 0 else 0.0
                glColor3f(color, color, color)
                
                glNormal3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr0, y * zr0, z0)
                
                glNormal3f(x * zr1, y * zr1, z1)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()
            
        glPopMatrix()
