from OpenGL.GL import *
from assets.primitives import Primitives
import numpy as np

class Fence:
    def __init__(self, width, length, height, gate_pos=0, gate_width=5):
        self.width = width
        self.length = length
        self.height = height
        self.gate_pos_x = gate_pos  # Posição do portão no eixo X
        self.gate_width = gate_width

    def draw(self):
        post_distance = 5.0
        gate_start = self.gate_pos_x - self.gate_width / 2
        gate_end = self.gate_pos_x + self.gate_width / 2

        # --- Postes da Cerca ---
        glColor3f(0.2, 0.2, 0.2)
        # Postes laterais (eixos +X e -X), completos
        for z in np.arange(-self.length / 2, self.length / 2 + post_distance, post_distance):
            for x_mult in [-1, 1]:
                glPushMatrix()
                glTranslatef((self.width / 2) * x_mult, self.height / 2, z)
                glScalef(0.2, self.height, 0.2)
                Primitives.draw_cube()
                glPopMatrix()

        # Postes de fundo (eixos +Z e -Z)
        for x in np.arange(-self.width / 2, self.width / 2 + post_distance, post_distance):
            # Fundo de cima (+Z), completo
            glPushMatrix()
            glTranslatef(x, self.height / 2, self.length / 2)
            glScalef(0.2, self.height, 0.2)
            Primitives.draw_cube()
            glPopMatrix()
            # Fundo de baixo (-Z), com a abertura para o portão
            if not (gate_start < x < gate_end):
                glPushMatrix()
                glTranslatef(x, self.height / 2, -self.length / 2)
                glScalef(0.2, self.height, 0.2)
                Primitives.draw_cube()
                glPopMatrix()

        # --- Tela da Cerca (Rede) ---
        glDisable(GL_LIGHTING)
        glColor3f(0.5, 0.5, 0.5)
        glLineWidth(1.0)
        glBegin(GL_LINES)

        # Linhas horizontais
        for y in np.arange(0.1, self.height, 0.5):
            # Lados
            glVertex3f(-self.width / 2, y, -self.length / 2); glVertex3f(-self.width / 2, y, self.length / 2)
            glVertex3f(self.width / 2, y, -self.length / 2); glVertex3f(self.width / 2, y, self.length / 2)
            # Fundo de cima
            glVertex3f(-self.width / 2, y, self.length / 2); glVertex3f(self.width / 2, y, self.length / 2)
            # Fundo de baixo (com abertura)
            glVertex3f(-self.width / 2, y, -self.length / 2); glVertex3f(gate_start, y, -self.length / 2)
            glVertex3f(gate_end, y, -self.length / 2); glVertex3f(self.width / 2, y, -self.length / 2)

        # Linhas verticais — lados
        for z in np.arange(-self.length / 2, self.length / 2 + 0.5, 0.5):
            # Lado esquerdo
            glVertex3f(-self.width / 2, 0.0, z); glVertex3f(-self.width / 2, self.height, z)
            # Lado direito
            glVertex3f(self.width / 2, 0.0, z); glVertex3f(self.width / 2, self.height, z)

        # Linhas verticais — fundo de cima
        for x in np.arange(-self.width / 2, self.width / 2 + 0.5, 0.5):
            glVertex3f(x, 0.0, self.length / 2); glVertex3f(x, self.height, self.length / 2)

        # Linhas verticais — fundo de baixo (com abertura)
        for x in np.arange(-self.width / 2, gate_start, 0.5):
            glVertex3f(x, 0.0, -self.length / 2); glVertex3f(x, self.height, -self.length / 2)
        for x in np.arange(gate_end, self.width / 2 + 0.5, 0.5):
            glVertex3f(x, 0.0, -self.length / 2); glVertex3f(x, self.height, -self.length / 2)

        glEnd()
        glEnable(GL_LIGHTING)

        # --- Portão de Correr ---
        glColor3f(0.0, 0.4, 0.1)  # Verde escuro
        glPushMatrix()
        # Posiciona o portão ao lado da abertura, no fundo de baixo
        glTranslatef(self.gate_pos_x - self.gate_width, self.height / 2, -self.length / 2 - 0.1)
        glScalef(self.gate_width, self.height, 0.1)
        Primitives.draw_cube()
        glPopMatrix()

    def get_bounding_box(self):
        center = [0, self.height / 2, 0]
        size = [self.width, self.height, self.length]
        return (center, size)
