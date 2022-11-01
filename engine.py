import pygame
from camera.camera import Camera
from light.single_direction import SingleDirectionLight
from matrix.transform import Transform
from object_loader import ObjectLoader
from projector import Projector
from shapes.mesh import Mesh
from shapes.triangle import Triangle
from util.color import Color
from util.drawing_mode import DrawingMode
from util.vector import Vector3
from util.matrix import *


class Engine:
    def __init__(self, max_fps: int, fov: float, near: float, far: float):
        self.running: bool = True
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.clock = pygame.time.Clock()
        self.max_fps = max_fps
        self.ticks = 0
        
        self.light = SingleDirectionLight(Vector3(0, 0, 1))
        self.camera = Camera(Vector3(0, 0, 0), Vector3(0, 1, 0), Vector3(0, -90, 0))
        self.axis_mesh = ObjectLoader.load('axis.obj')
        self.spaceship_mesh = ObjectLoader.load('spaceship.obj')

        self.drawing_mode = DrawingMode.Solid | DrawingMode.Wireframe

        self.projector = Projector(
            self.height / self.width, 
            fov,
            near,
            far)
        
    def run(self):
        pygame.init()

        while self.running:            
            self.ticks = self.clock.tick(self.max_fps)

            self.screen.fill(Color.BLACK)
            
            self.check_events()

            self.draw()

            pygame.display.flip()

        pygame.quit()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        move_speed = 0.01 * self.ticks
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.camera.move(Vector3(0, -move_speed, 0))
            self.light.direction = self.camera.get_look_direction()
        if keys[pygame.K_LCTRL]:
            self.camera.move(Vector3(0, move_speed, 0))
            self.light.direction = self.camera.get_look_direction()
        if keys[pygame.K_w]:
            self.camera.move(Vector3(0, 0, -move_speed))
            self.light.direction = self.camera.get_look_direction()
        if keys[pygame.K_s]:
            self.camera.move(Vector3(0, 0, move_speed))
            self.light.direction = self.camera.get_look_direction()
        if keys[pygame.K_a]:
            self.camera.move(Vector3(-move_speed, 0, 0))
            self.light.direction = self.camera.get_look_direction()
        if keys[pygame.K_d]:
            self.camera.move(Vector3(move_speed, 0, 0))
            self.light.direction = self.camera.get_look_direction()

        mouse_sensitivity_x = 0.1 * self.ticks
        mouse_sensitivity_y = 0.1 * self.ticks
        if keys[pygame.K_LEFT]:
            self.camera.rotate(Vector3(0, mouse_sensitivity_x, 0))
            self.light.direction = self.camera.get_look_direction()
        if keys[pygame.K_RIGHT]:
            self.camera.rotate(Vector3(0, -mouse_sensitivity_x, 0))
            self.light.direction = self.camera.get_look_direction()
        if keys[pygame.K_UP]:
            self.camera.rotate(Vector3(-mouse_sensitivity_y, 0, 0))
            self.light.direction = self.camera.get_look_direction()
        if keys[pygame.K_DOWN]:
            self.camera.rotate(Vector3(mouse_sensitivity_y, 0, 0))
            self.light.direction = self.camera.get_look_direction()

    def draw(self):
        axis = self.project(self.axis_mesh).sort()
        for triangle in axis.triangles:
            self.draw_triangle(triangle)

        # spaceship = self.project(self.spaceship_mesh).sort()
        # for triangle in spaceship.triangles:
        #     self.draw_triangle(triangle)

    def project(self, mesh: Mesh) -> Mesh:
        rotation_matrix_x = get_rotation_matrix_x(180)
        rotation_matrix_y = get_rotation_matrix_y(180)
        scaling_matrix = get_scaling_matrix(200, 200 * self.height / self.width, 1)
        translation_matrix = get_translation_matrix(self.width / 2, self.height / 2, 1)

        result_triangles = []
        for triangle in mesh.triangles:
            point0 = Transform(triangle.points[0].as_matrix())\
                .multiply(rotation_matrix_x)\
                .multiply(rotation_matrix_y)\
                .vector_matrix
            point1 = Transform(triangle.points[1].as_matrix())\
                .multiply(rotation_matrix_x)\
                .multiply(rotation_matrix_y)\
                .vector_matrix
            point2 = Transform(triangle.points[2].as_matrix())\
                .multiply(rotation_matrix_x)\
                .multiply(rotation_matrix_y)\
                .vector_matrix

            point0[2] -= 20
            point1[2] -= 20
            point2[2] -= 20
            
            normal = Triangle((Vector3.of(point0), Vector3.of(point1), Vector3.of(point2)), 0)\
                .get_normal()\
                .normalize()

            camera_offset = Vector3.of(point0)\
                .add(self.camera.pos, -1)\
                .as_matrix(0)
            
            if np.dot(normal.as_matrix(0), camera_offset) < 0:
                look_at_matrix = get_look_at_matrix(self.camera.pos, self.camera.target, self.camera.up)

                point0 = Transform(point0)\
                    .multiply(look_at_matrix)\
                    .multiply(self.projector.get_projection_matrix())\
                    .multiply(scaling_matrix)\
                    .multiply(translation_matrix)\
                    .vector_matrix
                point1 = Transform(point1)\
                    .multiply(look_at_matrix)\
                    .multiply(self.projector.get_projection_matrix())\
                    .multiply(scaling_matrix)\
                    .multiply(translation_matrix)\
                    .vector_matrix
                point2 = Transform(point2)\
                    .multiply(look_at_matrix)\
                    .multiply(self.projector.get_projection_matrix())\
                    .multiply(scaling_matrix)\
                    .multiply(translation_matrix)\
                    .vector_matrix
                
                luminance = np.dot(normal.as_matrix(0), self.light.direction.as_matrix(0))
                triangle = Triangle((Vector3.of(point0), Vector3.of(point1), Vector3.of(point2)), luminance)
                result_triangles.append(triangle)
        return Mesh(result_triangles)

    def draw_triangle(self, triangle: Triangle):
        if DrawingMode.Solid in self.drawing_mode:
            self.draw_solid(triangle)
        if DrawingMode.Wireframe in self.drawing_mode:
            self.draw_wireframe(triangle)

    def draw_solid(self, triangle: Triangle):
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
    
    def draw_wireframe(self, triangle: Triangle):
        points = triangle.points
        color = Color.WHITE
        if DrawingMode.Solid in self.drawing_mode:
            color = Color.BLACK

        pygame.draw.line(
            self.screen,
            color,
            (points[0].x, points[0].y),
            (points[1].x, points[1].y))

        pygame.draw.line(
            self.screen,
            color,
            (points[1].x, points[1].y),
            (points[2].x, points[2].y))

        pygame.draw.line(
            self.screen,
            color,
            (points[2].x, points[2].y),
            (points[0].x, points[0].y))
