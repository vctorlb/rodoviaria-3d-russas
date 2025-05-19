import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


def draw_soccer_field():
    # Dimensões oficiais
    field_length = 105.0
    field_width = 68.0
    line_height = 0.01
    
    # Elementos do campo
    center_circle_radius = 9.15
    halfway_line_width = field_width
    penalty_area_depth = 16.5
    penalty_area_width = 40.32
    goal_area_depth = 5.5
    goal_area_width = 18.32

    # Gramado
    glColor3f(0.0, 0.4, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-field_width/2, 0.0, -field_length/2)
    glVertex3f(field_width/2, 0.0, -field_length/2)
    glVertex3f(field_width/2, 0.0, field_length/2)
    glVertex3f(-field_width/2, 0.0, field_length/2)
    glEnd()

    # Linhas brancas
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.0)

    # Contorno do campo
    glBegin(GL_LINE_LOOP)
    glVertex3f(-field_width/2, line_height, -field_length/2)
    glVertex3f(field_width/2, line_height, -field_length/2)
    glVertex3f(field_width/2, line_height, field_length/2)
    glVertex3f(-field_width/2, line_height, field_length/2)
    glEnd()

    # Linha central (divisão do campo)
    glBegin(GL_LINES)
    glVertex3f(-field_width/2, line_height, 0.0)
    glVertex3f(field_width/2, line_height, 0.0)
    glEnd()

    # Círculo central (horizontal)
    glPushMatrix()
    glTranslatef(0.0, line_height, 0.0)
    glRotatef(90, 1, 0, 0)  # Rotação para plano XZ
    gluDisk(gluNewQuadric(), center_circle_radius - 0.1, center_circle_radius, 64, 1)
    glPopMatrix()

    # Áreas de meta
    for z in [-field_length/2, field_length/2]:
        # Pequena área
        glBegin(GL_LINE_LOOP)
        glVertex3f(-goal_area_width/2, line_height, z)
        glVertex3f(goal_area_width/2, line_height, z)
        glVertex3f(goal_area_width/2, line_height, z + (goal_area_depth if z < 0 else -goal_area_depth))
        glVertex3f(-goal_area_width/2, line_height, z + (goal_area_depth if z < 0 else -goal_area_depth))
        glEnd()

        # Grande área
        glBegin(GL_LINE_LOOP)
        glVertex3f(-penalty_area_width/2, line_height, z)
        glVertex3f(penalty_area_width/2, line_height, z)
        glVertex3f(penalty_area_width/2, line_height, z + (penalty_area_depth if z < 0 else -penalty_area_depth))
        glVertex3f(-penalty_area_width/2, line_height, z + (penalty_area_depth if z < 0 else -penalty_area_depth))
        glEnd()
