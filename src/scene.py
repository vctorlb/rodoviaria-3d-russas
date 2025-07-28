from OpenGL.GL import *
import numpy as np

from objects.skybox import Skybox
from objects.soccer_field import SoccerField
from objects.goal import Goal
from objects.reflector_post import ReflectorPost
from objects.locker_room import LockerRoom
from objects.fence import Fence
from objects.environment import Environment
from objects.ball import Ball

class Scene:
    def __init__(self, textures):
        self.textures = textures
        self.field_dims = (68.0, 105.0)
        self.sidewalk_width = 4.0

        self.skybox = Skybox(250, self.textures['skybox'])
        self.field = SoccerField(self.textures['grass'])
        self.environment = Environment(self.field_dims[0], self.field_dims[1], self.textures['sidewalk'], self.textures['street'])
        
        locker_room_x = -self.field_dims[0] / 2 - self.sidewalk_width / 2
        locker_room_z = -self.field_dims[1] / 3.5
        self.locker_room = LockerRoom(
        position=(28.0, 0.0, -60.5),
        scale=(3.0, 4.5, 4.0),
        rotation_y= 0.0
)

        
        self.fence = Fence(self.field_dims[0], self.field_dims[1], 6.0, gate_pos=locker_room_z)
        
        self.ball = Ball(position=(0, 0.22, 0))
        self.ball_speed = 10.0
        self.ball_direction = np.array([0.0, 0.0, 0.0])

        self.goals = [
            Goal(position=(0, 0, -self.field_dims[1]/2 + 1)),
            Goal(position=(0, 0, self.field_dims[1]/2 - 1), rotation_y=180)
        ]

        reflector_x_pos = self.field_dims[0] / 2 + self.sidewalk_width / 2
        reflector_z_offset = self.field_dims[1] / 3
        self.reflector_positions = [
            [ reflector_x_pos, 0,  reflector_z_offset], [ reflector_x_pos, 0, -reflector_z_offset],
            [-reflector_x_pos, 0,  reflector_z_offset], [-reflector_x_pos, 0, -reflector_z_offset]
        ]
        self.reflectors = [ReflectorPost(pos) for pos in self.reflector_positions]
        
        self.colliders = [self.locker_room]
        self.colliders = [self.locker_room, self.fence]


    def get_colliders(self):
        return self.colliders
    
    

        
    def draw(self, lighting_manager, is_day):
        self.skybox.draw()

        if is_day:
            lighting_manager.setup_day()
        else:
            lighting_manager.setup_night()
            target = np.array([0, 0, 0])
            light_y_pos = 15.0
            cutoff_angle = 40.0

            for i, pos in enumerate(self.reflector_positions):
                light_id = GL_LIGHT0 + i
                light_pos = [pos[0], light_y_pos, pos[2]]
                direction_vector = target - np.array(light_pos)
                norm_direction = direction_vector / np.linalg.norm(direction_vector)
                
                lighting_manager.setup_spotlight(light_id, light_pos, norm_direction, [1.0, 1.0, 0.8], 1.5, cutoff_angle, 10)
                lighting_manager.draw_spotlight_cone(light_pos, norm_direction, cutoff_angle)

        self.field.draw()
        self.environment.draw()
        self.locker_room.draw()
        self.fence.draw()
        self.ball.draw()
        
        for goal in self.goals:
            goal.draw()
        
        for reflector in self.reflectors:
            reflector.draw(is_day)