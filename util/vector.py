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

    def add(self, other: 'Vector3'):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def as_matrix(self, w: int = 1) -> np.ndarray:
        return np.array([self.x, self.y, self.z, w])

    def normalize(self) -> float:
        length = np.sqrt(self.x**2 + self.y**2 + self.z**2)
        
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length

    def __str__(self):
        return f"X: {self.x} / Y: {self.y} / Z: {self.z}"