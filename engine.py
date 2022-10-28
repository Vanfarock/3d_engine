import pygame
from camera.camera import Camera
from object_loader import ObjectLoader
from shapes.triangle import Triangle
from util.color import Color
from util.vector import Vector3
from util.matrix import *

MAX_FPS = 120

class Engine:
    def __init__(self):
        self.running: bool = True
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.clock = pygame.time.Clock()
        self.camera = Camera(Vector3(0, 0, 0))
        self.spaceship_mesh = ObjectLoader.load('spaceship.obj')
        self.cube_mesh = [
            # South
            Triangle([Vector3(0, 0, 0), Vector3(0, 1, 0), Vector3(1, 1, 0)], 1.0),
            Triangle([Vector3(0, 0, 0), Vector3(1, 1, 0), Vector3(1, 0, 0)], 1.0),

            # East                                                     
            Triangle([Vector3(1, 0, 0), Vector3(1, 1, 0), Vector3(1, 1, 1)], 1.0),
            Triangle([Vector3(1, 0, 0), Vector3(1, 1, 1), Vector3(1, 0, 1)], 1.0),

            # North
            Triangle([Vector3(1, 0, 1), Vector3(1, 1, 1), Vector3(0, 1, 1)], 1.0),
            Triangle([Vector3(1, 0, 1), Vector3(0, 1, 1), Vector3(0, 0, 1)], 1.0),

            # West
            Triangle([Vector3(0, 0, 1), Vector3(0, 1, 1), Vector3(0, 1, 0)], 1.0),
            Triangle([Vector3(0, 0, 1), Vector3(0, 1, 0), Vector3(0, 0, 0)], 1.0),

            # Top                                                    
            Triangle([Vector3(0, 1, 0), Vector3(0, 1, 1), Vector3(1, 1, 1)], 1.0),
            Triangle([Vector3(0, 1, 0), Vector3(1, 1, 1), Vector3(1, 1, 0)], 1.0),

            # Bottom
            Triangle([Vector3(1, 0, 1), Vector3(0, 0, 1), Vector3(0, 0, 0)], 1.0),
            Triangle([Vector3(1, 0, 1), Vector3(0, 0, 0), Vector3(1, 0, 0)], 1.0),

            # # South
            # Triangle([Vector3(-0.5, -0.5, -0.5), Vector3(-0.5, 0.5, -0.5), Vector3(0.5, 0.5, -0.5)], 1.0),
            # Triangle([Vector3(-0.5, -0.5, -0.5), Vector3(0.5, 0.5, -0.5), Vector3(0.5, -0.5, -0.5)], 1.0),

            # # East                                                     
            # Triangle([Vector3(0.5, -0.5, -0.5), Vector3(0.5, 0.5, -0.5), Vector3(0.5, 0.5, 0.5)], 1.0),
            # Triangle([Vector3(0.5, -0.5, -0.5), Vector3(0.5, 0.5, 0.5), Vector3(0.5, -0.5, 0.5)], 1.0),

            # # North
            # Triangle([Vector3(0.5, -0.5, 0.5), Vector3(0.5, 0.5, 0.5), Vector3(-0.5, 0.5, 0.5)], 1.0),
            # Triangle([Vector3(0.5, -0.5, 0.5), Vector3(-0.5, 0.5, 0.5), Vector3(-0.5, -0.5, 0.5)], 1.0),

            # # West
            # Triangle([Vector3(-0.5, -0.5, 0.5), Vector3(-0.5, 0.5, 0.5), Vector3(-0.5, 0.5, -0.5)], 1.0),
            # Triangle([Vector3(-0.5, -0.5, 0.5), Vector3(-0.5, 0.5, -0.5), Vector3(-0.5, -0.5, -0.5)], 1.0),

            # # Top                                                    
            # Triangle([Vector3(-0.5, 0.5, -0.5), Vector3(-0.5, 0.5, 0.5), Vector3(0.5, 0.5, 0.5)], 1.0),
            # Triangle([Vector3(-0.5, 0.5, -0.5), Vector3(0.5, 0.5, 0.5), Vector3(0.5, 0.5, -0.5)], 1.0),

            # # Bottom
            # Triangle([Vector3(0.5, -0.5, 0.5), Vector3(-0.5, -0.5, 0.5), Vector3(-0.5, -0.5, -0.5)], 1.0),
            # Triangle([Vector3(0.5, -0.5, 0.5), Vector3(-0.5, -0.5, -0.5), Vector3(0.5, -0.5, -0.5)], 1.0),
        ]
        
        self.aspect_ratio = self.height / self.width
        self.projection_matrix = get_projection_matrix(
            self.aspect_ratio,
            fov=90,
            near=0.1,
            far=1_000
        )

        self.ticks = 0
        self.theta_x = 90
        self.theta_y = 90
        self.theta_z = 0

    def run(self):
        pygame.init()

        while self.running:            
            self.ticks = self.clock.tick(MAX_FPS)

            self.screen.fill(Color.BLACK)
            
            self.check_events()

            self.draw()

            self.theta_x += 0.1 * self.ticks
            self.theta_y += 0.1 * self.ticks
            self.theta_z += 0.1 * self.ticks

            pygame.display.flip()

        pygame.quit()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self):
        # cube_points = self.project(self.cube_mesh)
        
        # for triangle in cube_points:
            # self.draw_triangle(triangle)

        spaceship_points = self.project(self.spaceship_mesh)
        spaceship_points.sort(key=lambda t: t.average_z())
        for triangle in spaceship_points:
            self.draw_triangle(triangle)

    def project(self, triangles: 'list[Triangle]') -> 'list[Triangle]':
        rotation_matrix_x = get_rotation_matrix_x(self.theta_x)
        rotation_matrix_z = get_rotation_matrix_z(self.theta_z)
        scaling_matrix = get_scaling_matrix(200, 200 * self.aspect_ratio, 1)
        translation_matrix = get_translation_matrix(self.width / 2, self.height / 2, 1)

        result_triangles = []
        for triangle in triangles:
            result_points = []

            point0 = triangle.points[0].as_matrix()
            point1 = triangle.points[1].as_matrix()
            point2 = triangle.points[2].as_matrix()

            point0 = np.matmul(
                rotation_matrix_z, point0)
            point1 = np.matmul(
                rotation_matrix_z, point1)
            point2 = np.matmul(
                rotation_matrix_z, point2)

            point0 = np.matmul(
                rotation_matrix_x, point0)
            point1 = np.matmul(
                rotation_matrix_x, point1)
            point2 = np.matmul(
                rotation_matrix_x, point2)

            point0[2] -= 20
            point1[2] -= 20
            point2[2] -= 20
            
            line1 = Vector3(0, 0, 0)
            line1.x = point1[0] - point0[0]
            line1.y = point1[1] - point0[1]
            line1.z = point1[2] - point0[2]

            line2 = Vector3(0, 0, 0)
            line2.x = point2[0] - point0[0]
            line2.y = point2[1] - point0[1]
            line2.z = point2[2] - point0[2]

            normal = Vector3(0, 0, 0)
            normal.x = line1.y * line2.z - line1.z * line2.y
            normal.y = line1.z * line2.x - line1.x * line2.z
            normal.z = line1.x * line2.y - line1.y * line2.x
            normal.normalize()

            camera_offset = [point0[0] - self.camera.position.x, point0[1] - self.camera.position.y, point0[2] - self.camera.position.z, 0]
            
            if np.dot(normal.as_matrix(0), camera_offset) < 0:
                light = Vector3(0, 0, 1)
                light.normalize()

                luminance = np.dot(normal.as_matrix(0), light.as_matrix(0))

                point0 = np.matmul(
                    self.projection_matrix, point0)
                point1 = np.matmul(
                    self.projection_matrix, point1)
                point2 = np.matmul(
                    self.projection_matrix, point2)

                point0 = np.matmul(
                    scaling_matrix, point0)
                point1 = np.matmul(
                    scaling_matrix, point1)
                point2 = np.matmul(
                    scaling_matrix, point2)

                point0 = np.matmul(
                    translation_matrix, point0)
                point1 = np.matmul(
                    translation_matrix, point1)
                point2 = np.matmul(
                    translation_matrix, point2)

                w0 = point0[3]
                if w0 != 0:
                    division_scaling_matrix = get_scaling_matrix(1/w0, 1/w0, 1/w0)
                    point0 = np.matmul(division_scaling_matrix, point0)
                result_points.append(Vector3(point0[0], point0[1], point0[2]))

                w1 = point1[3]
                if w1 != 0:
                    division_scaling_matrix = get_scaling_matrix(1/w1, 1/w1, 1/w1)
                    point1 = np.matmul(division_scaling_matrix, point1)
                result_points.append(Vector3(point1[0], point1[1], point1[2]))

                w2 = point2[3]
                if w2 != 0:
                    division_scaling_matrix = get_scaling_matrix(1/w2, 1/w2, 1/w2)
                    point2 = np.matmul(division_scaling_matrix, point2)
                result_points.append(Vector3(point2[0], point2[1], point2[2]))
            
                result_triangles.append(Triangle(result_points, luminance))
        return result_triangles

    def draw_triangle(self, triangle: Triangle):
        points = triangle.points

        r = Color.WHITE[0] * triangle.luminance
        r = max(0, min(r, 255))
        g = Color.WHITE[1] * triangle.luminance
        g = max(0, min(g, 255))
        b = Color.WHITE[2] * triangle.luminance
        b = max(0, min(b, 255))
        color = (r, g, b)

        pygame.draw.polygon(
            self.screen,
            color,
            [
                (points[0].x, points[0].y),
                (points[1].x, points[1].y),
                (points[2].x, points[2].y),
            ]
        )
        
        # pygame.draw.line(
        #     self.screen,
        #     Color.WHITE,
        #     (points[0].x, points[0].y),
        #     (points[1].x, points[1].y))

        # pygame.draw.line(
        #     self.screen,
        #     Color.WHITE,
        #     (points[1].x, points[1].y),
        #     (points[2].x, points[2].y))

        # pygame.draw.line(
        #     self.screen,
        #     Color.WHITE,
        #     (points[2].x, points[2].y),
        #     (points[0].x, points[0].y))