import numpy as np

from util.vector import Vector3

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

def get_look_at_matrix(pos: Vector3, target: Vector3, up: Vector3):
    forward_vector = target.copy()
    forward_vector.subtract(pos)
    forward_vector.normalize()

    projection_size = np.dot(up.as_matrix(0), forward_vector.as_matrix(0))
    tmp_forward_matrix = forward_vector.as_matrix() * projection_size
    tmp_forward_vector = Vector3(tmp_forward_matrix[0], tmp_forward_matrix[1], tmp_forward_matrix[2])
    new_up_vector = up.copy()
    new_up_vector.subtract(tmp_forward_vector)
    new_up_vector.normalize()

    new_up_matrix = [new_up_vector.x, new_up_vector.y, new_up_vector.z]
    forward_matrix = [forward_vector.x, forward_vector.y, forward_vector.z]
    right_matrix = np.cross(new_up_matrix, forward_matrix)
    right_vector = Vector3(right_matrix[0], right_matrix[1], right_matrix[2])

    look_at_matrix = np.array([
        [right_vector.x, right_vector.y, right_vector.z, -pos.x],
        [new_up_vector.x, new_up_vector.y, new_up_vector.z, -pos.y],
        [forward_vector.x, forward_vector.y, forward_vector.z, -pos.z],
        [0, 0, 0, 1],
    ])
    return look_at_matrix
    
def get_camera_rotation_matrix(pitch: float, yaw: float):
    pitch_rad = np.deg2rad(pitch)
    yaw_rad = np.deg2rad(yaw)

    rotation_matrix = np.zeros((4, 4))
    rotation_matrix[0, 0] = 1
    rotation_matrix[1, 1] = 1
    rotation_matrix[1, 2] = 1
    rotation_matrix[0, 3] = np.cos(yaw_rad) * np.cos(pitch_rad)
    rotation_matrix[1, 3] = np.sin(pitch_rad)
    rotation_matrix[2, 3] = np.sin(yaw_rad) * np.cos(pitch_rad)
    return rotation_matrix

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