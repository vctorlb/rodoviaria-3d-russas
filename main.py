import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from camera import Camera
from campo import draw_soccer_field

def main():
    if not glfw.init():
        return

    width, height = 1280, 720
    window = glfw.create_window(width, height, "Campo de Futebol 3D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    camera = Camera(width, height)
    glfw.set_key_callback(window, camera.key_callback)
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(90, width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        camera.process_input(window)
        
        glClearColor(0.53, 0.81, 0.98, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        camera.update_camera()
        draw_soccer_field()
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()