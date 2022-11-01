import numpy as np

from util.vector import Vector3

def get_rotation_matrix_x(theta: float):
    theta_rad = np.deg2rad(theta)

    rotation_matrix_x = np.zeros((4, 4))
    rotation_matrix_x[0, 0] = 1
    rotation_matrix_x[1, 1] = np.cos(theta_rad)
    rotation_matrix_x[1, 2] = np.sin(theta_rad)
    rotation_matrix_x[2, 1] = -np.sin(theta_rad)
    rotation_matrix_x[2, 2] = np.cos(theta_rad)
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

def get_look_at_matrix(pos: Vector3, target: Vector3, up: Vector3):
    camera_target = target.copy()
    camera_target.add(pos, -1)
    camera_target.normalize()

    projection_size = np.dot(up.as_matrix(0), camera_target.as_matrix(0))
    tmp_target_matrix = camera_target.as_matrix() * projection_size
    tmp_target = Vector3(tmp_target_matrix[0], tmp_target_matrix[1], tmp_target_matrix[2])
    camera_up = up.copy()
    camera_up.add(tmp_target, -1)
    camera_up.normalize()

    tmp_right_matrix = np.cross([camera_up.x, camera_up.y, camera_up.z], [camera_target.x, camera_target.y, camera_target.z])
    camera_right = Vector3(tmp_right_matrix[0], tmp_right_matrix[1], tmp_right_matrix[2])

    look_at = np.zeros((4, 4))
    look_at[0, 0] = camera_right.x
    look_at[0, 1] = camera_right.y
    look_at[0, 2] = camera_right.z
    look_at[1, 0] = camera_up.x
    look_at[1, 1] = camera_up.y
    look_at[1, 2] = camera_up.z
    look_at[2, 0] = camera_target.x
    look_at[2, 1] = camera_target.y
    look_at[2, 2] = camera_target.z
    look_at[0, 3] = -pos.x
    look_at[1, 3] = -pos.y
    look_at[2, 3] = -pos.z
    look_at[3, 3] = 1
    return look_at
