import numpy as np

def get_projection_matrix(aspect_ratio: float, fov: float, near: float, far: float):
    fov_rad = 1 / np.tan(np.deg2rad(fov) * 0.5)
    
    projection_matrix = np.zeros((4, 4))
    projection_matrix[0, 0] = aspect_ratio * fov_rad
    projection_matrix[1, 1] = fov_rad
    projection_matrix[2, 2] = far / (far - near)
    projection_matrix[3, 2] = (-far * near) / (far - near)
    projection_matrix[2, 3] = 1
    projection_matrix[3, 3] = 0
    return projection_matrix


def get_rotation_matrix_x(theta: float):
    theta_rad = np.deg2rad(theta)

    rotation_matrix_x = np.zeros((4, 4))
    rotation_matrix_x[0, 0] = 1
    rotation_matrix_x[1, 1] = np.cos(theta_rad * 0.5)
    rotation_matrix_x[1, 2] = np.sin(theta_rad * 0.5)
    rotation_matrix_x[2, 1] = -np.sin(theta_rad * 0.5)
    rotation_matrix_x[2, 2] = np.cos(theta_rad * 0.5)
    rotation_matrix_x[3, 3] = 1
    return rotation_matrix_x

def get_rotation_matrix_y(theta: float):
    theta_rad = np.deg2rad(theta)
    
    rotation_matrix_y = np.zeros((4, 4))
    rotation_matrix_y[0, 0] = np.cos(theta_rad)
    rotation_matrix_y[0, 2] = np.sin(theta_rad)
    rotation_matrix_y[1, 1] = 1
    rotation_matrix_y[2, 0] = -np.sin(theta_rad)
    rotation_matrix_y[2, 2] = np.cos(theta_rad)
    rotation_matrix_y[3, 3] = 1
    return rotation_matrix_y

def get_rotation_matrix_z(theta: float):
    theta_rad = np.deg2rad(theta)
    
    rotation_matrix_z = np.zeros((4, 4))
    rotation_matrix_z[0, 0] = np.cos(theta_rad)
    rotation_matrix_z[0, 1] = np.sin(theta_rad)
    rotation_matrix_z[1, 0] = -np.sin(theta_rad)
    rotation_matrix_z[1, 1] = np.cos(theta_rad)
    rotation_matrix_z[2, 2] = 1
    rotation_matrix_z[3, 3] = 1
    return rotation_matrix_z

def get_scaling_matrix(x: float, y: float, z: float):
    scaling_matrix = np.zeros((4, 4))
    scaling_matrix[0, 0] = x
    scaling_matrix[1, 1] = y
    scaling_matrix[2, 2] = z
    scaling_matrix[3, 3] = 1
    return scaling_matrix

def get_translation_matrix(x: float, y: float, z: float):
    translation_matrix = np.zeros((4, 4))
    translation_matrix[0, 0] = 1
    translation_matrix[1, 1] = 1
    translation_matrix[2, 2] = 1
    translation_matrix[0, 3] = x
    translation_matrix[1, 3] = y
    translation_matrix[2, 3] = z
    translation_matrix[3, 3] = 1
    return translation_matrix