import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Garante que as importações de outros diretórios funcionem
sys.path.append('.') 

from assets.texture_loader import TextureLoader
from camera import Camera
from scene import Scene
from lighting import Lighting

class App:
    def __init__(self, width=1600, height=900):
        self.last_frame_time = 0.0
        self.is_day = True # A cena começa de dia
        
        if not glfw.init():
            raise Exception("GLFW não pôde ser inicializado.")

        # Dicas para solicitar uma versão do OpenGL compatível
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)

        self.window = glfw.create_window(width, height, "Areninha 3D - Computação Gráfica", None, None)
        
        if not self.window:
            glfw.terminate()
            raise Exception("A janela GLFW não pôde ser criada.")

        glfw.make_context_current(self.window)
        glfw.set_window_size_callback(self.window, self._on_resize)

        self.camera = Camera(width, height)
        # O callback de teclado agora é centralizado nesta classe para evitar conflitos
        glfw.set_key_callback(self.window, self._key_callback)
        glfw.set_cursor_pos_callback(self.window, self.camera.mouse_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self._setup_opengl(width, height)
        self._load_assets()

        self.lighting = Lighting()
        self.scene = Scene(self.textures)
        print("Aplicação inicializada. Use N para alternar Dia/Noite, V para visão de cima, ESC para sair.")

    def _key_callback(self, window, key, scancode, action, mods):
        # --- CONTROLO DE TECLADO CENTRALIZADO ---
        # Controles do aplicativo
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_N and action == glfw.PRESS:
            self.is_day = not self.is_day
            print(f"Modo alterado para: {'Dia' if self.is_day else 'Noite'}")
        if key == glfw.KEY_V and action == glfw.PRESS:
            self.camera.is_top_down_view = not self.camera.is_top_down_view
        
        # Atualiza o dicionário de teclas da câmara para movimentação
        if key in [glfw.KEY_W, glfw.KEY_A, glfw.KEY_S, glfw.KEY_D]:
            if action == glfw.PRESS:
                self.camera.keys[key] = True
            elif action == glfw.RELEASE:
                self.camera.keys[key] = False
        # ----------------------------------------

    def _setup_opengl(self, width, height):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        self._on_resize(self.window, width, height)

    def _load_assets(self):
        self.textures = {
            'grass': TextureLoader.load('imgs/grama.jpg'),
            'street': TextureLoader.load('imgs/asfalto.jpg'),
            'sidewalk': TextureLoader.load('imgs/calcada.png'),
            'skybox': {
                'front': TextureLoader.load('imgs/skybox/skyboxF.png', repeat=False),
                'back':  TextureLoader.load('imgs/skybox/skyboxBack.png', repeat=False),
                'left':  TextureLoader.load('imgs/skybox/skyboxL.png', repeat=False),
                'right': TextureLoader.load('imgs/skybox/skyboxR.png', repeat=False),
                'top':   TextureLoader.load('imgs/skybox/skyboxT.png', repeat=False),
                'bottom':TextureLoader.load('imgs/skybox/skyboxB.png', repeat=False)
            }
        }

    def _on_resize(self, window, width, height):
        if height == 0: height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(75, width / height, 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)

    def run(self):
        while not glfw.window_should_close(self.window):
            current_time = glfw.get_time()
            delta_time = current_time - self.last_frame_time
            self.last_frame_time = current_time
            
            glfw.poll_events()
            colliders = self.scene.get_colliders()
            self.camera.process_input(self.window, delta_time, colliders)
            
            if self.is_day:
                glClearColor(0.53, 0.81, 0.98, 1.0)
            else:
                glClearColor(0.05, 0.05, 0.15, 1.0)
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            glLoadIdentity()
            
            if self.camera.is_top_down_view:
                gluLookAt(0, 90, 1, 0, 0, 0, 0, 1, 0)
            else:
                pos = self.camera.camera_pos
                front = self.camera.camera_front
                up = self.camera.camera_up
                gluLookAt(pos[0], pos[1], pos[2], 
                          pos[0] + front[0], pos[1] + front[1], pos[2] + front[2], 
                          up[0], up[1], up[2])
            
            self.scene.draw(self.lighting, self.is_day)
            glfw.swap_buffers(self.window)
            
        glfw.terminate()
