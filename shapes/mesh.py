from shapes.triangle import Triangle


class Mesh:
    def __init__(self, triangles: 'list[Triangle]'):
        self.triangles = triangles

    def sort(self) -> 'Mesh':
        self.triangles.sort(key=lambda t: t.average_z())
        return self
