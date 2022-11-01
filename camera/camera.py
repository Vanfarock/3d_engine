import numpy as np
from util.vector import Vector3


class Camera:
    def __init__(self, pos: Vector3, up: Vector3, rotation: Vector3):
        self.pos = pos
        self.up = up
        self.rotation = rotation
        self.__update_target()

    def __update_target(self):
        self.target = Vector3(0, 0, 0)
        self.target.add(self.pos)
        self.target.add(self.get_look_direction())

    def move(self, move: Vector3):
        self.pos.add(move)
        self.__update_target()

    def rotate(self, rotation: Vector3):
        self.rotation.add(rotation)
        if self.rotation.x > 89: self.rotation.x = 89
        if self.rotation.x < -89: self.rotation.x = -89
        self.__update_target()

    def get_look_direction(self) -> Vector3:
        pitch_rad = -np.deg2rad(self.rotation.x)
        yaw_rad = -np.deg2rad(self.rotation.y)
        
        return Vector3(
            np.cos(pitch_rad) * np.cos(yaw_rad),
            np.sin(pitch_rad),
            np.cos(pitch_rad) * np.sin(yaw_rad))