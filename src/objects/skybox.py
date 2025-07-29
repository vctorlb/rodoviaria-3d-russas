from OpenGL.GL import *

class Skybox:
    def __init__(self, size, textures):
        self.size = size
        self.textures = textures

    def draw(self, camera_pos):
        """
        Desenha a skybox centralizada na posição da câmera e alinhada com o chão.
        """
        glPushMatrix()
        
        # Move a skybox para a posição (X, Z) da câmera.
        # No eixo Y, movemos para o nível 0 e depois subimos pela metade do tamanho da skybox
        # para que a base dela fique em y=0.
        glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])

        s = self.size
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        
        # Desativa a escrita no buffer de profundidade para que a skybox fique sempre no fundo.
        glDepthMask(GL_FALSE)
        
        # --- CÓDIGO DE MAPEAMENTO DE TEXTURA CORRETO ---
        # A coordenada 't' (vertical) da textura é invertida aqui (0 vira 1, 1 vira 0)
        # para compensar a forma como a biblioteca Pillow carrega as imagens.

        # Front
        glBindTexture(GL_TEXTURE_2D, self.textures['front'])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1); glVertex3f(-s, -s, -s)
        glTexCoord2f(1, 0); glVertex3f(-s,  s, -s)
        glTexCoord2f(0, 0); glVertex3f( s,  s, -s)
        glTexCoord2f(0, 1); glVertex3f( s, -s, -s)
        glEnd()

        # Back
        glBindTexture(GL_TEXTURE_2D, self.textures['back'])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1); glVertex3f( s, -s,  s)
        glTexCoord2f(1, 0); glVertex3f( s,  s,  s)
        glTexCoord2f(0, 0); glVertex3f(-s,  s,  s)
        glTexCoord2f(0, 1); glVertex3f(-s, -s,  s)
        glEnd()
        
        # Left
        glBindTexture(GL_TEXTURE_2D, self.textures['left'])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1); glVertex3f(-s, -s,  s)
        glTexCoord2f(1, 0); glVertex3f(-s,  s,  s)
        glTexCoord2f(0, 0); glVertex3f(-s,  s, -s)
        glTexCoord2f(0, 1); glVertex3f(-s, -s, -s)
        glEnd()

        # Right
        glBindTexture(GL_TEXTURE_2D, self.textures['right'])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1); glVertex3f( s, -s, -s)
        glTexCoord2f(1, 0); glVertex3f( s,  s, -s)
        glTexCoord2f(0, 0); glVertex3f( s,  s,  s)
        glTexCoord2f(0, 1); glVertex3f( s, -s,  s)
        glEnd()

        # Top
        glBindTexture(GL_TEXTURE_2D, self.textures['top'])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex3f(-s,  s, -s)
        glTexCoord2f(0, 0); glVertex3f(-s,  s,  s)
        glTexCoord2f(1, 0); glVertex3f( s,  s,  s)
        glTexCoord2f(1, 1); glVertex3f( s,  s, -s)
        glEnd()

        # Bottom
        glBindTexture(GL_TEXTURE_2D, self.textures['bottom'])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-s, -s, -s)
        glTexCoord2f(0, 1); glVertex3f(-s, -s,  s)
        glTexCoord2f(1, 1); glVertex3f( s, -s,  s)
        glTexCoord2f(1, 0); glVertex3f( s, -s, -s)
        glEnd()
        
        # Reativa a escrita no buffer de profundidade para os outros objetos da cena.
        glDepthMask(GL_TRUE)
        glDisable(GL_TEXTURE_2D)
        
        glPopMatrix()