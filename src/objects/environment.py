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
        self.top_sidewalk_extra_depth = 15.0 # Para o lado Z positivo (frente)

        # --- NOVO: Largura extra para a calçada na parte de BAIXO (Z negativo, onde está o vestiário) ---
        self.bottom_sidewalk_extra_depth = 10.0 # Ajuste este valor conforme a necessidade. Ex: 5.0, 10.0
        # --- FIM NOVO ---

        # Variáveis de controle de repetição da textura
        self.sidewalk_tile_unit_x = 5.0 
        self.sidewalk_tile_unit_z = 5.0 
        self.street_tile_unit_x = 10.0 
        self.street_tile_unit_z = 10.0 

    def draw(self):
        glPushMatrix()
        
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glNormal3f(0, 1, 0) # Normal para superfícies planas no eixo Y

        # --- Desenha a Calçada ---
        if self.tex_sidewalk is not None:
            glBindTexture(GL_TEXTURE_2D, self.tex_sidewalk)
            
            # Coordenadas base (largura e comprimento do campo e calçadas)
            inner_x = self.field_width / 2
            outer_x_normal = inner_x + self.sidewalk_width 
            inner_z = self.field_length / 2
            outer_z_normal = inner_z + self.sidewalk_width
            
            # Coordenada Z para a calçada da frente (Z positivo)
            outer_z_top = inner_z + self.sidewalk_width + self.top_sidewalk_extra_depth
            
            # --- NOVO: Coordenada Z para a calçada de trás (Z negativo) ---
            # O ponto mais distante da calçada no Z negativo
            outer_z_bottom = outer_z_normal + self.bottom_sidewalk_extra_depth 
            # Note que este valor é usado como coordenada Z negativa, então será -outer_z_bottom no glVertex3f
            # O vestiário estaria entre -inner_z e -outer_z_bottom
            # --- FIM NOVO ---

            # --- Calçada de trás (Z negativo, AGORA MAIOR) ---
            # Dimensão em X: de -outer_x_normal a outer_x_normal (total: 2 * outer_x_normal)
            # Dimensão em Z: de -outer_z_bottom a -inner_z (total: outer_z_bottom - inner_z)
            glBegin(GL_QUADS)
            glTexCoord2f(-outer_x_normal / self.sidewalk_tile_unit_x, -outer_z_bottom / self.sidewalk_tile_unit_z)
            glVertex3f(-outer_x_normal, 0.01, -outer_z_bottom) # NOVO VÉRTICE Z

            glTexCoord2f( outer_x_normal / self.sidewalk_tile_unit_x, -outer_z_bottom / self.sidewalk_tile_unit_z)
            glVertex3f( outer_x_normal, 0.01, -outer_z_bottom) # NOVO VÉRTICE Z

            glTexCoord2f( outer_x_normal / self.sidewalk_tile_unit_x, -inner_z / self.sidewalk_tile_unit_z)
            glVertex3f( outer_x_normal, 0.01, -inner_z)

            glTexCoord2f(-outer_x_normal / self.sidewalk_tile_unit_x, -inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(-outer_x_normal, 0.01, -inner_z)
            glEnd()

            # --- Calçada da esquerda (X negativo) ---
            # Dimensão em X: de -outer_x_normal a -inner_x (total: sidewalk_width)
            # Dimensão em Z: de -inner_z a inner_z (total: field_length)
            glBegin(GL_QUADS)
            glTexCoord2f(-outer_x_normal / self.sidewalk_tile_unit_x, -inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(-outer_x_normal, 0.01, -inner_z)

            glTexCoord2f(-inner_x / self.sidewalk_tile_unit_x, -inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(-inner_x, 0.01, -inner_z)

            glTexCoord2f(-inner_x / self.sidewalk_tile_unit_x, inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(-inner_x, 0.01, inner_z)

            glTexCoord2f(-outer_x_normal / self.sidewalk_tile_unit_x, inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(-outer_x_normal, 0.01, inner_z)
            glEnd()

            # --- Calçada da direita (X positivo) ---
            # Dimensão em X: de inner_x a outer_x_normal (total: sidewalk_width)
            # Dimensão em Z: de -inner_z a inner_z (total: field_length)
            glBegin(GL_QUADS)
            glTexCoord2f(inner_x / self.sidewalk_tile_unit_x, -inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(inner_x, 0.01, -inner_z)

            glTexCoord2f(outer_x_normal / self.sidewalk_tile_unit_x, -inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(outer_x_normal, 0.01, -inner_z)

            glTexCoord2f(outer_x_normal / self.sidewalk_tile_unit_x, inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(outer_x_normal, 0.01, inner_z)

            glTexCoord2f(inner_x / self.sidewalk_tile_unit_x, inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(inner_x, 0.01, inner_z)
            glEnd()

            # --- Calçada da frente (Z positivo, MAIOR) ---
            # Dimensão em X: de -outer_x_normal a outer_x_normal (total: 2 * outer_x_normal)
            # Dimensão em Z: de inner_z a outer_z_top (total: outer_z_top - inner_z)
            glBegin(GL_QUADS)
            glTexCoord2f(-outer_x_normal / self.sidewalk_tile_unit_x, inner_z / self.sidewalk_tile_unit_z)
            glVertex3f(-outer_x_normal, 0.01, inner_z)

            glTexCoord2f( outer_x_normal / self.sidewalk_tile_unit_x, inner_z / self.sidewalk_tile_unit_z)
            glVertex3f( outer_x_normal, 0.01, inner_z)

            glTexCoord2f( outer_x_normal / self.sidewalk_tile_unit_x, outer_z_top / self.sidewalk_tile_unit_z)
            glVertex3f( outer_x_normal, 0.01, outer_z_top)

            glTexCoord2f(-outer_x_normal / self.sidewalk_tile_unit_x, outer_z_top / self.sidewalk_tile_unit_z)
            glVertex3f(-outer_x_normal, 0.01, outer_z_top)
            glEnd()

        # --- Desenha a Estrada ---
        if self.tex_street is not None:
            glBindTexture(GL_TEXTURE_2D, self.tex_street)
            road_start_x = self.field_width / 2 + self.sidewalk_width
            road_end_x = road_start_x + self.street_width
            
            # Dimensão em X: de road_start_x a road_end_x (total: street_width)
            # Dimensão em Z: de -self.field_length * 1.5 a self.field_length * 1.5 (total: 3 * self.field_length)
            
            glBegin(GL_QUADS)
            glTexCoord2f(road_start_x / self.street_tile_unit_x, (-self.field_length * 1.5) / self.street_tile_unit_z)
            glVertex3f(road_start_x, 0.0, -self.field_length * 1.5)

            glTexCoord2f(road_end_x / self.street_tile_unit_x, (-self.field_length * 1.5) / self.street_tile_unit_z)
            glVertex3f(road_end_x, 0.0, -self.field_length * 1.5)

            glTexCoord2f(road_end_x / self.street_tile_unit_x, (self.field_length * 1.5) / self.street_tile_unit_z)
            glVertex3f(road_end_x, 0.0, self.field_length * 1.5)

            glTexCoord2f(road_start_x / self.street_tile_unit_x, (self.field_length * 1.5) / self.street_tile_unit_z)
            glVertex3f(road_start_x, 0.0, self.field_length * 1.5)
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()