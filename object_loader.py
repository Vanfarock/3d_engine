from shapes.triangle import Triangle
from util.vector import Vector3

class ObjectLoader:
    def load(filename: str) -> 'list[Triangle]':
        with open(filename) as f:
            vertices = []
            triangles = []
            for line in f.readlines():
                if line.startswith('v'):
                    items = line.split(' ')
                    x, y, z = float(items[1]), float(items[2]), float(items[3])
                    vertices.append(Vector3(x, y, z))

                if line.startswith('f'):
                    items = line.split(' ')
                    i, j, k = int(items[1]), int(items[2]), int(items[3])
                    triangles.append(Triangle((vertices[i - 1], vertices[j - 1], vertices[k - 1]), 1))
            return triangles