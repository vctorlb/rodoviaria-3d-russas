import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# --- Função que desenha um cubo em immediate mode ---
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
def draw_vestiario():
    # 1) Base branca
    glPushMatrix()
    glTranslatef(0, 1.0, 0)
    glScalef(4.0, 2.0, 2.0)
    glColor3f(1.0, 1.0, 1.0)
    cube()
    glPopMatrix()

    # 2) Faixa rosa
    glPushMatrix()
    glTranslatef(0, 1.4, 0)
    glScalef(4.0, 0.4, 2.0)
    glColor3f(1.0, 1.0, 1.0)
    cube()
    glPopMatrix()

    # 3) Porta verde
    glPushMatrix()
    glTranslatef(1.2, 0.6, 1.05)
    glScalef(0.6, 1.2, 0.1)
    glColor3f(0.0, 0.5, 0.0)  
    cube()
    glPopMatrix()

    # 4) Janela de vidro
    glPushMatrix()
    glTranslatef(-1.2, 1.2, 1.05)
    glScalef(0.8, 0.6, 0.1)
    glColor3f(0.8, 0.8, 0.8) 
    cube()
    glPopMatrix()

def main():
    if not glfw.init():
        raise Exception("GLFW init falhou")
    width, height = 800, 600
    win = glfw.create_window(width, height, "Vestiário (fixed pipeline)", None, None)
    if not win:
        raise Exception("Janela falhou")
    glfw.make_context_current(win)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/height, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

    angle_yaw   = 45.0
    angle_pitch = 20.0
    dist        = 10.0

    while not glfw.window_should_close(win):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        yaw   = np.radians(angle_yaw)
        pitch = np.radians(angle_pitch)
        camX = dist * math.cos(pitch) * math.sin(yaw)
        camY = dist * math.sin(pitch)
        camZ = dist * math.cos(pitch) * math.cos(yaw)

        gluLookAt(camX, camY, camZ,   0,1,0,   0,1,0)

        draw_vestiario()

        if glfw.get_key(win, glfw.KEY_LEFT)  == glfw.PRESS: angle_yaw   -= 0.5
        if glfw.get_key(win, glfw.KEY_RIGHT) == glfw.PRESS: angle_yaw   += 0.5
        if glfw.get_key(win, glfw.KEY_UP)    == glfw.PRESS: angle_pitch = min(angle_pitch+0.5, 89)
        if glfw.get_key(win, glfw.KEY_DOWN)  == glfw.PRESS: angle_pitch = max(angle_pitch-0.5, -89)
        if glfw.get_key(win, glfw.KEY_W)     == glfw.PRESS: dist = max(2, dist-0.025)
        if glfw.get_key(win, glfw.KEY_S)     == glfw.PRESS: dist = min(30, dist+0.025)

        glfw.swap_buffers(win)

    glfw.terminate()

if __name__ == "__main__":
    main()
