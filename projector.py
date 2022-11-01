import numpy as np

class Projector:
    def __init__(self, aspect_ratio: float, fov: float, near: float, far: float):
        self.aspect_ratio = aspect_ratio
        self.fov = fov
        self.near = near
        self.far = far

        self.projecion_matrix = self.__get_projection_matrix()

    def __get_projection_matrix(self):
        fov_rad = 1 / np.tan(np.deg2rad(self.fov) * 0.5)
        
        projection_matrix = np.zeros((4, 4))
        projection_matrix[0, 0] = self.aspect_ratio * fov_rad
        projection_matrix[1, 1] = fov_rad
        projection_matrix[2, 2] = self.far / (self.far - self.near)
        projection_matrix[3, 2] = (-self.far * self.near) / (self.far - self.near)
        projection_matrix[2, 3] = 1
        projection_matrix[3, 3] = 0
        return projection_matrix

    def get_projection_matrix(self):
        return self.projecion_matrix