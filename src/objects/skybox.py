from OpenGL.GL import *

class Skybox:
    def __init__(self, size, textures):
        self.size = size
        self.textures = textures

    def draw(self):
        s = self.size
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        
        glDepthMask(GL_FALSE)
        
        # Front
        glBindTexture(GL_TEXTURE_2D, self.textures['front'])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0); glVertex3f(-s, -s, -s)
        glTexCoord2f(1, 1); glVertex3f(-s,  s, -s)
        glTexCoord2f(0, 1); glVertex3f( s,  s, -s)
        glTexCoord2f(0, 0); glVertex3f( s, -s, -s)
        glEnd()

        # Back
        glBindTexture(GL_TEXTURE_2D, self.textures['back'])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0); glVertex3f( s, -s,  s)
        glTexCoord2f(1, 1); glVertex3f( s,  s,  s)
        glTexCoord2f(0, 1); glVertex3f(-s,  s,  s)
        glTexCoord2f(0, 0); glVertex3f(-s, -s,  s)
        glEnd()
        
        # Left
        glBindTexture(GL_TEXTURE_2D, self.textures['left'])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0); glVertex3f(-s, -s,  s)
        glTexCoord2f(1, 1); glVertex3f(-s,  s,  s)
        glTexCoord2f(0, 1); glVertex3f(-s,  s, -s)
        glTexCoord2f(0, 0); glVertex3f(-s, -s, -s)
        glEnd()

        # Right
        glBindTexture(GL_TEXTURE_2D, self.textures['right'])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0); glVertex3f( s, -s, -s)
        glTexCoord2f(1, 1); glVertex3f( s,  s, -s)
        glTexCoord2f(0, 1); glVertex3f( s,  s,  s)
        glTexCoord2f(0, 0); glVertex3f( s, -s,  s)
        glEnd()

        # Top
        glBindTexture(GL_TEXTURE_2D, self.textures['top'])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-s,  s, -s) # t=0
        glTexCoord2f(0, 1); glVertex3f(-s,  s,  s) # t=1
        glTexCoord2f(1, 1); glVertex3f( s,  s,  s) # t=1
        glTexCoord2f(1, 0); glVertex3f( s,  s, -s) # t=0
        glEnd()

        # Bottom
        glBindTexture(GL_TEXTURE_2D, self.textures['bottom'])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex3f(-s, -s, -s) # t=1
        glTexCoord2f(0, 0); glVertex3f(-s, -s,  s) # t=0
        glTexCoord2f(1, 0); glVertex3f( s, -s,  s) # t=0
        glTexCoord2f(1, 1); glVertex3f( s, -s, -s) # t=1
        glEnd()
        glDepthMask(GL_TRUE)
        glDisable(GL_TEXTURE_2D)
