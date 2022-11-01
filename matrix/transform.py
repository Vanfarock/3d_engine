import numpy as np

class Transform:
    def __init__(self, vector_matrix: np.ndarray):
        self.vector_matrix = vector_matrix
    
    def multiply(self, transformation: np.ndarray) -> 'Transform':
        self.vector_matrix = np.matmul(transformation, self.vector_matrix)
        return self
