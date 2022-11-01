import numpy as np


class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def copy(self) -> 'Vector3':
        return Vector3(self.x, self.y, self.z)

    def of(matrix: np.ndarray) -> 'Vector3':
        if matrix[3] != 0:
            matrix *= 1/matrix[3]
        return Vector3(matrix[0], matrix[1], matrix[2])

    def add(self, other: 'Vector3', scale: float=1) -> 'Vector3':
        self.x += (other.x * scale)
        self.y += (other.y * scale)
        self.z += (other.z * scale)
        return self

    def as_matrix(self, w: int = 1) -> np.ndarray:
        return np.array([self.x, self.y, self.z, w])

    def normalize(self) -> 'Vector3':
        length = np.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return self

    def __str__(self):
        return f"X: {self.x} / Y: {self.y} / Z: {self.z}"