from util.vector import Vector3


class Triangle:
    def __init__(self, points: 'tuple[Vector3, Vector3, Vector3]', luminance: float):
        self.points = points
        self.luminance = luminance

    def get_normal(self) -> Vector3:
        point0 = self.points[0]
        point1 = self.points[1]
        point2 = self.points[2]

        line1 = Vector3(0, 0, 0)
        line1.x = point1.x - point0.x
        line1.y = point1.y - point0.y
        line1.z = point1.z - point0.z

        line2 = Vector3(0, 0, 0)
        line2.x = point2.x - point0.x
        line2.y = point2.y - point0.y
        line2.z = point2.z - point0.z

        normal = Vector3(0, 0, 0)
        normal.x = line1.y * line2.z - line1.z * line2.y
        normal.y = line1.z * line2.x - line1.x * line2.z
        normal.z = line1.x * line2.y - line1.y * line2.x
        return normal

    def average_z(self):
        return (self.points[0].z + self.points[1].z + self.points[2].z) / 3
