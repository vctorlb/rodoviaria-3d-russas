# src/objects/locker_room.py

from OpenGL.GL import *
from assets.primitives import Primitives
import numpy as np

class LockerRoom:
    def __init__(self, position, scale=(1.0, 1.0, 1.0), rotation_y=0, governo_texture=None):
        self.position = np.array(position, dtype=float)
        self.scale = scale
        self.rotation_y = rotation_y
        self.governo_texture = governo_texture
        
        width_orig = 4.0 * scale[0]
        depth_orig = 2.0 * scale[2]
        height_scaled = 1.0 * scale[1] * 2

        if abs(self.rotation_y) % 180 != 0:
            self.bb_size = [depth_orig, height_scaled, width_orig]
        else:
            self.bb_size = [width_orig, height_scaled, depth_orig]
            
        self.bb_center = self.position + np.array([0, self.bb_size[1]/2, 0])

    def get_bounding_box(self):
        return (self.bb_center, self.bb_size)

    def draw_textured_quad(self, texture_id, width, height):
        """Desenha um quad com textura aplicada"""
        if texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-width/2, -height/2, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(width/2, -height/2, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(width/2, height/2, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-width/2, height/2, 0.0)
        glEnd()
        
        if texture_id:
            glDisable(GL_TEXTURE_2D)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation_y, 0, 1, 0)
        glScalef(self.scale[0], self.scale[1], self.scale[2])

        # Base
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        glScalef(4.0, 1.0, 2.0)
        glColor3f(0.95, 0.95, 0.95)
        Primitives.draw_cube()
        glPopMatrix()

        # Porta
        glPushMatrix()
        glTranslatef(-1.2, 0.3, 1.01)
        glScalef(0.6, 1.2, 0.1)
        glColor3f(0.0, 0.5, 0.0)
        Primitives.draw_cube()
        glPopMatrix()

        # Janela
        glPushMatrix()
        glTranslatef(1.2, 0.6, 1.01)
        glScalef(0.8, 0.6, 0.1)
        glColor3f(0.6, 0.8, 0.9)
        Primitives.draw_cube()
        glPopMatrix()

        # Placa do Governo do Estado na parede frontal
        if self.governo_texture:
            glPushMatrix()
            glTranslatef(0, 0.7, 1.02)  # Centralizada na parede frontal, um pouco mais alta
            glColor3f(1.0, 1.0, 1.0)  # Cor branca para não alterar a textura
            self.draw_textured_quad(self.governo_texture, 1.5, 0.8)  # Tamanho da placa
            glPopMatrix()
        
        glPopMatrix()
