from OpenGL.GL import *

class Environment:
    def __init__(self, field_width, field_length, tex_sidewalk, tex_street):
        self.field_width = field_width
        self.field_length = field_length
        self.tex_sidewalk = tex_sidewalk
        self.tex_street = tex_street
        self.sidewalk_width = 4.0
        self.street_width = 15.0
        self.offset_from_field = 0.0 
        # Largura extra para a calçada na parte de cima (Z positivo)
        self.top_sidewalk_extra_depth = 10.0

    def draw(self):
        glPushMatrix()
        
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glNormal3f(0, 1, 0)

        # --- Desenha a Calçada ---
        if self.tex_sidewalk is not None:
            glBindTexture(GL_TEXTURE_2D, self.tex_sidewalk)
            
            # Coordenadas base
            inner_x = self.field_width / 2
            outer_x_normal = inner_x + self.sidewalk_width
            inner_z = self.field_length / 2
            outer_z_normal = inner_z + self.sidewalk_width
            
            # Coordenada Z para a parte de cima, que é maior
            outer_z_top = inner_z + self.sidewalk_width + self.top_sidewalk_extra_depth

            # Calçada de trás (Z negativo, normal)
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0); glVertex3f(-outer_x_normal, 0.01, -outer_z_normal)
            glTexCoord2f(20.0, 1.0); glVertex3f( outer_x_normal, 0.01, -outer_z_normal)
            glTexCoord2f(20.0, 0.0); glVertex3f( outer_x_normal, 0.01, -inner_z)
            glTexCoord2f(0.0, 0.0); glVertex3f(-outer_x_normal, 0.01, -inner_z)
            glEnd()

            # Calçada da esquerda (X negativo, normal)
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0); glVertex3f(-outer_x_normal, 0.01, -inner_z)
            glTexCoord2f(1.0, 1.0); glVertex3f(-inner_x, 0.01, -inner_z)
            glTexCoord2f(1.0, 0.0); glVertex3f(-inner_x, 0.01,  inner_z)
            glTexCoord2f(0.0, 0.0); glVertex3f(-outer_x_normal, 0.01,  inner_z)
            glEnd()

            # Calçada da direita (X positivo, conecta com a estrada)
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0); glVertex3f(inner_x, 0.01, -inner_z)
            glTexCoord2f(1.0, 1.0); glVertex3f(outer_x_normal, 0.01, -inner_z)
            glTexCoord2f(1.0, 0.0); glVertex3f(outer_x_normal, 0.01,  inner_z)
            glTexCoord2f(0.0, 0.0); glVertex3f(inner_x, 0.01,  inner_z)
            glEnd()

            # Calçada da frente (Z positivo, MAIOR)
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0); glVertex3f(-outer_x_normal, 0.01, inner_z)
            glTexCoord2f(20.0, 1.0); glVertex3f( outer_x_normal, 0.01, inner_z)
            glTexCoord2f(20.0, 0.0); glVertex3f( outer_x_normal, 0.01, outer_z_top)
            glTexCoord2f(0.0, 0.0); glVertex3f(-outer_x_normal, 0.01, outer_z_top)
            glEnd()

        # --- Desenha a Estrada ---
        if self.tex_street is not None:
            glBindTexture(GL_TEXTURE_2D, self.tex_street)
            road_start_x = self.field_width / 2 + self.sidewalk_width
            road_end_x = road_start_x + self.street_width
            
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(road_start_x, 0.0, -self.field_length * 1.5)
            glTexCoord2f(2.0, 0.0); glVertex3f(road_end_x, 0.0, -self.field_length * 1.5)
            glTexCoord2f(2.0, 30.0); glVertex3f(road_end_x, 0.0, self.field_length * 1.5)
            glTexCoord2f(0.0, 30.0); glVertex3f(road_start_x, 0.0, self.field_length * 1.5)
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
