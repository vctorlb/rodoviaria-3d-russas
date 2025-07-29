import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import os
import numpy as np

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
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

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
        print("Aplicação inicializada. Use N para alternar Dia/Noite, V para visão de cima, M para alternar modo mouse, ESC para sair.")

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
        if key == glfw.KEY_B and action == glfw.PRESS:
            self.camera.follow_ball = not self.camera.follow_ball
            if self.camera.follow_ball:
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
                print("Modo câmera seguindo a bola ativado (use as setas para mover)")
            else:
                print("Modo câmera livre ativado")

        # Atalho para alternar entre mouse normal ou modo jogo (apenas quando não estiver seguindo a bola)
        if not self.camera.follow_ball and key == glfw.KEY_M and action == glfw.PRESS:
            current_mode = glfw.get_input_mode(window, glfw.CURSOR)
            if current_mode == glfw.CURSOR_DISABLED:
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            else:
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Controle da bola com as setas quando no modo follow_ball
        if self.camera.follow_ball:
            if key in [glfw.KEY_UP, glfw.KEY_DOWN, glfw.KEY_LEFT, glfw.KEY_RIGHT]:
                if action == glfw.PRESS:
                    self.scene.ball_direction = np.array([0.0, 0.0, 0.0])
                    if key == glfw.KEY_UP: self.scene.ball_direction[2] = -1.0
                    elif key == glfw.KEY_DOWN: self.scene.ball_direction[2] = 1.0
                    elif key == glfw.KEY_LEFT: self.scene.ball_direction[0] = -1.0
                    elif key == glfw.KEY_RIGHT: self.scene.ball_direction[0] = 1.0
                elif action == glfw.RELEASE:
                    if key in [glfw.KEY_UP, glfw.KEY_DOWN]: self.scene.ball_direction[2] = 0.0
                    elif key in [glfw.KEY_LEFT, glfw.KEY_RIGHT]: self.scene.ball_direction[0] = 0.0

        # Atualiza o dicionário de teclas da câmara para movimentação (apenas quando não estiver seguindo a bola)
        if not self.camera.follow_ball and key in [glfw.KEY_W, glfw.KEY_A, glfw.KEY_S, glfw.KEY_D]:
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
        imgs_dir = os.path.abspath(os.path.join(self.base_dir, '..', 'imgs'))
        skybox_dir = os.path.join(imgs_dir, 'skybox')
        self.textures = {
            'grass': TextureLoader.load(os.path.join(imgs_dir, 'grama.jpg')),
            'street': TextureLoader.load(os.path.join(imgs_dir, 'asfalto.jpg')),
            'sidewalk': TextureLoader.load(os.path.join(imgs_dir, 'calcada.png')),
            'skybox': {
                'front': TextureLoader.load(os.path.join(skybox_dir, 'skyboxF.png'), repeat=False),
                'back':  TextureLoader.load(os.path.join(skybox_dir, 'skyboxBack.png'), repeat=False),
                'left':  TextureLoader.load(os.path.join(skybox_dir, 'skyboxL.png'), repeat=False),
                'right': TextureLoader.load(os.path.join(skybox_dir, 'skyboxR.png'), repeat=False),
                'top':   TextureLoader.load(os.path.join(skybox_dir, 'skyboxT.png'), repeat=False),
                'bottom':TextureLoader.load(os.path.join(skybox_dir, 'skyboxB.png'), repeat=False)
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
            
            # Atualiza a posição da bola baseado na direção
            if np.any(self.scene.ball_direction):
                ball_speed = 10.0
                new_pos = np.array(self.scene.ball.position)
                new_pos[0] += self.scene.ball_direction[0] * ball_speed * delta_time
                new_pos[2] += self.scene.ball_direction[2] * ball_speed * delta_time
                # Limita o movimento da bola ao campo
                new_pos[0] = np.clip(new_pos[0], -self.scene.field_dims[0]/2, self.scene.field_dims[0]/2)
                new_pos[2] = np.clip(new_pos[2], -self.scene.field_dims[1]/2, self.scene.field_dims[1]/2)
                self.scene.ball.position = new_pos.tolist()
            
            # Atualiza a câmera
            if not self.camera.follow_ball:
                self.camera.process_input(self.window, delta_time, colliders)
            else:
                # Posiciona a câmera atrás da bola
                ball_pos = np.array(self.scene.ball.position)
                ball_dir = self.scene.ball_direction
                if not np.any(ball_dir):  # Se a bola não está se movendo
                    ball_dir = np.array([0, 0, 1])  # Direção padrão
                
                # Calcula a posição da câmera atrás da bola
                camera_offset = np.array([0, 2, 5])  # Altura e distância da câmera
                self.camera.camera_pos = ball_pos + camera_offset
                
                # Faz a câmera olhar para a bola
                self.camera.camera_front = -camera_offset / np.linalg.norm(camera_offset)
            
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
            
            self.scene.draw(self.lighting, self.is_day, self.camera.camera_pos)
            glfw.swap_buffers(self.window)
            
        glfw.terminate()
