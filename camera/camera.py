from util.vector import Vector3


class Camera:
    def __init__(self, position: Vector3, rotation: Vector3):
        self.position = position
        self.rotation = rotation
        