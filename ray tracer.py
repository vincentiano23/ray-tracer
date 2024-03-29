import pygame
import sys
import math

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FOV = math.pi / 2  # Field of View

# Define a sphere
class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def intersect(self, origin, direction):
        oc = origin - self.center
        a = direction.dot(direction)
        b = 2.0 * oc.dot(direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c

        if discriminant > 0:
            t1 = (-b - math.sqrt(discriminant)) / (2.0 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2.0 * a)
            return min(t1, t2) if t1 > 0 else t2

        return float('inf')


# Ray tracing function
def ray_trace(origin, direction, spheres):
    closest_t = float('inf')
    closest_sphere = None

    for sphere in spheres:
        t = sphere.intersect(origin, direction)
        if t < closest_t:
            closest_t = t
            closest_sphere = sphere

    if closest_sphere:
        hit_point = origin + direction * closest_t
        normal = (hit_point - closest_sphere.center).normalize()
        return closest_sphere.color

    return BACKGROUND_COLOR


# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ray Tracer")

    clock = pygame.time.Clock()

    # Define spheres in the scene
    spheres = [
        Sphere(center=(0, 0, 5), radius=1, color=(255, 0, 0)),
        Sphere(center=(2, 1, 5), radius=0.5, color=(0, 255, 0)),
        Sphere(center=(-2, -1, 5), radius=1.5, color=(0, 0, 255)),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOR)

        for x in range(WIDTH):
            for y in range(HEIGHT):
                # Map screen coordinates to normalized device coordinates
                ndc_x = (2 * x - WIDTH) / WIDTH
                ndc_y = (HEIGHT - 2 * y) / HEIGHT

                # Calculate ray direction
                aspect_ratio = WIDTH / HEIGHT
                tan_half_fov = math.tan(FOV / 2)
                ray_direction = ((ndc_x * aspect_ratio * tan_half_fov, ndc_y * tan_half_fov, -1)).normalize()

                # Ray tracing
                color = ray_trace(origin=(0, 0, 0), direction=ray_direction, spheres=spheres)

                screen.set_at((x, y), color)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
