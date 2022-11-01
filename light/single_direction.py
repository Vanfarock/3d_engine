from util.vector import Vector3

class SingleDirectionLight:
    def __init__(self, direction: Vector3):
        self.direction = direction.normalize()
