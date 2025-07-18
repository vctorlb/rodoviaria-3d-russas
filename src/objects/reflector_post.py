from OpenGL.GL import *
from assets.primitives import Primitives

class ReflectorPost:
    def __init__(self, position):
        self.position = position
        self.post_height = 15.0

    def draw(self, is_day):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])

        # Base
        glColor3f(0.6, 0.6, 0.6)
        glPushMatrix()
        glTranslatef(0, 0.2, 0)
        glScalef(0.5, 0.4, 0.5)
        Primitives.draw_cube()
        glPopMatrix()

        # Poste
        glColor3f(0.5, 0.5, 0.55)
        glPushMatrix()
        glTranslatef(0, self.post_height / 2, 0)
        glRotatef(-90, 1, 0, 0)
        Primitives.draw_cylinder(0.1, 0.1, self.post_height, 16, 1)
        glPopMatrix()

        # Caixa do refletor
        glColor3f(0.3, 0.3, 0.3)
        glPushMatrix()
        glTranslatef(0, self.post_height, 0)
        glRotatef(-15, 1, 0, 0)
        glScalef(1.2, 0.6, 1.2)
        Primitives.draw_cube()
        glPopMatrix()

        if not is_day:
            glDisable(GL_LIGHTING)
            glColor3f(1.0, 1.0, 0.7)
            glPushMatrix()
            glTranslatef(0, self.post_height - 0.2, 0.3)
            glRotatef(-15, 1, 0, 0)
            Primitives.draw_sphere(0.2, 16, 16)
            glPopMatrix()
            glEnable(GL_LIGHTING)
        
        glPopMatrix()
