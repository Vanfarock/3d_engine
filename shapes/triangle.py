from util.vector import Vector3


class Triangle:
    def __init__(self, points: 'list[Vector3]', luminance: float):
        self.points = points
        self.luminance = luminance
        
    def average_z(self):
        return (self.points[0].z + self.points[1].z + self.points[2].z) / 3
