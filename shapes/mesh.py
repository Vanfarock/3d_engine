from shapes.triangle import Triangle


class Mesh:
    def __init__(self, triangles: 'list[Triangle]'):
        self.triangles = triangles