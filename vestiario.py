# vestiario.py

from OpenGL.GL import *
from OpenGL.GLU import *

def cube():
    vertices = [
        [-0.5,-0.5,-0.5],[ 0.5,-0.5,-0.5],
        [ 0.5, 0.5,-0.5],[-0.5, 0.5,-0.5],
        [-0.5,-0.5, 0.5],[ 0.5,-0.5, 0.5],
        [ 0.5, 0.5, 0.5],[-0.5, 0.5, 0.5]
    ]
    faces = [
        [0,1,2,3],[4,5,6,7],
        [0,1,5,4],[2,3,7,6],
        [0,3,7,4],[1,2,6,5]
    ]
    glBegin(GL_QUADS)
    for face in faces:
        for idx in face:
            glVertex3fv(vertices[idx])
    glEnd()

def vestiario():
    # Base branca
    glPushMatrix()
    glTranslatef(0, 1.0, 0)
    glScalef(4.0, 2.0, 2.0)
    glColor3f(1.0, 1.0, 1.0)
    cube()
    glPopMatrix()

    # Faixa superior (branca)
    glPushMatrix()
    glTranslatef(0, 1.4, 0)
    glScalef(4.0, 0.4, 2.0)
    glColor3f(1.0, 1.0, 1.0)
    cube()
    glPopMatrix()

    # Porta verde
    glPushMatrix()
    glTranslatef(-1.2, 0.6, -1.05)
    glScalef(0.6, 1.2, 0.1)
    glColor3f(0.0, 0.5, 0.0)
    cube()
    glPopMatrix()

    # Janela “aberta” em cinza claro
    glPushMatrix()
    glTranslatef(1.2, 1.2, -1.05)
    glScalef(0.8, 0.6, 0.1)
    glColor3f(0.8, 0.8, 0.8)
    cube()
    glPopMatrix()
