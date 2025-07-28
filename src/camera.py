import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Camera:
    def __init__(self, width, height, position=np.array([45.0, 1.7, 25.0])):
        # Posição inicial na estrada, olhando para o vestiário e a entrada
        self.camera_pos = position
        self.camera_front = np.array([-1.0, 0.0, 0.0])
        self.camera_up = np.array([0.0, 1.0, 0.0])
        
        self.yaw = -180.0
        self.pitch = 0.0
        
        self.camera_speed = 5.0
        self.sensitivity = 0.1
        self.last_x, self.last_y = width / 2, height / 2
        self.first_mouse = True
        
        # Dicionário para guardar o estado das teclas, agora preenchido pela classe App
        self.keys = {}
        self.is_top_down_view = False
        self.follow_ball = False  # Novo modo de câmera que segue a bola
        self.ball_offset = np.array([0, 2, 5])  # Offset da câmera em relação à bola

    def process_input(self, window, delta_time, colliders):
        """Processa o input de movimento da câmera com base no estado das teclas."""
        if self.is_top_down_view:
            return

        speed = self.camera_speed * delta_time
        potential_pos = np.copy(self.camera_pos)
        
        # Verifica o estado das teclas no dicionário
        if self.keys.get(glfw.KEY_W, False): potential_pos += speed * self.camera_front
        if self.keys.get(glfw.KEY_S, False): potential_pos -= speed * self.camera_front
        if self.keys.get(glfw.KEY_A, False): potential_pos -= np.cross(self.camera_front, self.camera_up) * speed
        if self.keys.get(glfw.KEY_D, False): potential_pos += np.cross(self.camera_front, self.camera_up) * speed

        potential_pos[1] = 1.7 # Impede que a câmera "voe"

        # Aplica a nova posição apenas se não houver colisão
        if not self._check_collision(potential_pos, colliders):
            self.camera_pos = potential_pos

    def _check_collision(self, pos, colliders):
        """Verifica se a posição da câmera colide com algum objeto."""
        for collider in colliders:
            center, size = collider.get_bounding_box()
            min_c = np.array(center) - np.array(size) / 2
            max_c = np.array(center) + np.array(size) / 2
            if (min_c[0] <= pos[0] <= max_c[0] and 
                min_c[1] <= pos[1] <= max_c[1] and 
                min_c[2] <= pos[2] <= max_c[2]):
                return True # Colisão detectada
        return False

    def mouse_callback(self, window, xpos, ypos):
        """Processa o movimento do mouse para olhar ao redor."""
        if self.is_top_down_view:
            self.first_mouse = True # Reseta o mouse ao sair da visão de cima
            return

        if self.first_mouse:
            self.last_x, self.last_y = xpos, ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos
        self.last_x, self.last_y = xpos, ypos

        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        # self.pitch = np.clip(self.pitch + yoffset, -89.0, 89.0)

        # Atualiza o vetor frontal da câmera com base nos ângulos de yaw e pitch
        direction = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.camera_front = direction / np.linalg.norm(direction)
