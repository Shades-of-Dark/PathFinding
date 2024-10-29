# Updated avoid_obstacle method with zero velocity handling
import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
MAX_SPEED = 5
MAX_FORCE = 0.1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Vector2(pygame.math.Vector2):
    pass


class Entity:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

    def apply_force(self, force):
        self.acceleration += force

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration *= 0

    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.position.x), int(self.position.y)), 8)

    def seek(self, target):
        desired = (target - self.position).normalize() * MAX_SPEED
        steer = desired - self.velocity
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def avoid_obstacle(self, obstacles, feeler_length=50):
        # Enhanced obstacle avoidance with raycasting (feelers)
        avoidance = Vector2(0, 0)

        # Check if velocity is non-zero before normalizing
        if self.velocity.length() > 0:
            feeler = self.position + self.velocity.normalize() * feeler_length
        else:
            # Default feeler direction if at rest
            feeler = self.position + Vector2(0, -1) * feeler_length

        for obs in obstacles:
            to_obstacle = obs.position - self.position
            distance = to_obstacle.length()

            # Check if the feeler intersects the obstacle
            if distance < feeler_length + obs.radius:
                # Steer perpendicular to the obstacle
                avoid_dir = to_obstacle.rotate(90).normalize()
                avoid_force = avoid_dir * MAX_SPEED / (distance / 10)  # Stronger force when closer
                avoidance += avoid_force

        if avoidance.length() > MAX_FORCE:
            avoidance.scale_to_length(MAX_FORCE)
        return avoidance

    def context_steering(self, target, obstacles):
        seek_force = self.seek(target) * 0.8
        avoid_force = self.avoid_obstacle(obstacles) * 4  # Stronger weight on avoidance
        combined_force = seek_force + avoid_force
        return combined_force


class Obstacle:
    def __init__(self, x, y, radius=15):
        self.position = Vector2(x, y)
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.position.x), int(self.position.y)), self.radius)


# Initialize entities and obstacles
entity = Entity(100, 100)
target = Vector2(WIDTH - 100, HEIGHT - 100)
obstacles = [Obstacle(400, 300), Obstacle(400, 350)]

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    target.x, target.y = pygame.mouse.get_pos()

    pygame.draw.circle(screen, (0, 255, 0), (int(target.x), int(target.y)), 8)
    for obs in obstacles:
        obs.draw()

    # Calculate steering force
    steering_force = entity.context_steering(target, obstacles)
    entity.apply_force(steering_force)

    entity.update()
    entity.draw()

    pygame.display.flip()
    clock.tick(60)
  #  pygame.time.delay(30)

pygame.quit()
