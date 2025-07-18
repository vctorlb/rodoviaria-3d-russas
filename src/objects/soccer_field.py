from OpenGL.GL import *
from OpenGL.GLU import *

class SoccerField:
    def __init__(self, texture_id):
        self.texture_id = texture_id
        self.field_length = 105.0
        self.field_width = 68.0
        self.line_height = 0.02

        self.center_circle_radius = 9.15
        self.penalty_area_depth = 16.5
        self.penalty_area_width = 40.32
        self.goal_area_depth = 5.5
        self.goal_area_width = 18.32

    def draw(self):
        self._draw_grass()
        self._draw_lines()

    def _draw_grass(self):
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        
        if self.texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glBegin(GL_QUADS)
            glNormal3f(0.0, 1.0, 0.0)
            glTexCoord2f(0.0, 0.0); glVertex3f(-self.field_width/2, 0.0, -self.field_length/2)
            glTexCoord2f(15.0, 0.0); glVertex3f(self.field_width/2, 0.0, -self.field_length/2)
            glTexCoord2f(15.0, 30.0); glVertex3f(self.field_width/2, 0.0, self.field_length/2)
            glTexCoord2f(0.0, 30.0); glVertex3f(-self.field_width/2, 0.0, self.field_length/2)
            glEnd()
        
        glDisable(GL_TEXTURE_2D)

    def _draw_lines(self):
        glDisable(GL_LIGHTING)

        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(3.0)

        # Contorno
        glBegin(GL_LINE_LOOP)
        glVertex3f(-self.field_width/2, self.line_height, -self.field_length/2)
        glVertex3f(self.field_width/2, self.line_height, -self.field_length/2)
        glVertex3f(self.field_width/2, self.line_height, self.field_length/2)
        glVertex3f(-self.field_width/2, self.line_height, self.field_length/2)
        glEnd()

        # Linha do meio
        glBegin(GL_LINES)
        glVertex3f(-self.field_width/2, self.line_height, 0.0)
        glVertex3f(self.field_width/2, self.line_height, 0.0)
        glEnd()

        # Círculo central
        glPushMatrix()
        glTranslatef(0.0, self.line_height, 0.0)
        glRotatef(90, 1, 0, 0)
        quad = gluNewQuadric()
        gluPartialDisk(quad, self.center_circle_radius - 0.15, self.center_circle_radius, 64, 1, 0, 360)
        gluDeleteQuadric(quad)
        glPopMatrix()

        # Áreas
        for z_mult in [-1, 1]:
            z_pos = z_mult * self.field_length / 2
            
            # Grande área
            z_end_penalty = z_pos - z_mult * self.penalty_area_depth
            glBegin(GL_LINE_LOOP)
            glVertex3f(-self.penalty_area_width/2, self.line_height, z_pos)
            glVertex3f(self.penalty_area_width/2, self.line_height, z_pos)
            glVertex3f(self.penalty_area_width/2, self.line_height, z_end_penalty)
            glVertex3f(-self.penalty_area_width/2, self.line_height, z_end_penalty)
            glEnd()

            # Pequena área
            z_end_goal = z_pos - z_mult * self.goal_area_depth
            glBegin(GL_LINE_LOOP)
            glVertex3f(-self.goal_area_width/2, self.line_height, z_pos)
            glVertex3f(self.goal_area_width/2, self.line_height, z_pos)
            glVertex3f(self.goal_area_width/2, self.line_height, z_end_goal)
            glVertex3f(-self.goal_area_width/2, self.line_height, z_end_goal)
            glEnd()

        glEnable(GL_LIGHTING)
