from OpenGL.GL import *
from assets.primitives import Primitives

class Goal:
    def __init__(self, position, rotation_y=0):
        self.position = position
        self.rotation_y = rotation_y
        
        self.height = 3.0
        self.width = 7.32
        self.post_thickness = 0.2

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation_y, 0, 1, 0)
        
        glColor3f(0.95, 0.95, 0.95)

        # Travessão
        glPushMatrix()
        glTranslatef(0, self.height, 0)
        glScalef(self.width, self.post_thickness, self.post_thickness)
        Primitives.draw_cube()
        glPopMatrix()

        # Poste Esquerdo
        glPushMatrix()
        glTranslatef(-self.width / 2, self.height / 2, 0)
        glScalef(self.post_thickness, self.height, self.post_thickness)
        Primitives.draw_cube()
        glPopMatrix()

        # Poste Direito
        glPushMatrix()
        glTranslatef(self.width / 2, self.height / 2, 0)
        glScalef(self.post_thickness, self.height, self.post_thickness)
        Primitives.draw_cube()
        glPopMatrix()
        
        glPopMatrix()
