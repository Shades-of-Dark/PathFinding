import pygame
import sys
import math as m


class Vector(pygame.math.Vector2):
    pass


class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.pos = [self.x, self.y]
        # works like north north east, east, south east, etc.
        self.interest_map = []

        self.danger_map = []
        self.speed = 0.2
        self.color = color

        self.masks = []

        self.DISTANCE_CONSTRAINT = 800

    def chase(self, interests):

        self.interest_map.clear()
        self.masks.clear()
        for i in range(8):
            if len(interests) > i:
                e = interests[i]

                distX, distY = e.x - self.x, e.y - self.y
                i_v = Vector(distX, distY)
                dist = i_v.length()
                weight = (self.DISTANCE_CONSTRAINT - dist) / self.DISTANCE_CONSTRAINT
                i_v.normalize_ip()

                self.interest_map.append((i_v, weight))
                self.masks.append(True)
            else:
                self.interest_map.append((Vector(0, 0), 0))
                self.masks.append(True)

    def avoid(self, dangers):
        self.danger_map.clear()

        for i in range(8):

            if len(dangers) > i:
                e = dangers[i]
                distX, distY = e.x - self.x, e.y - self.y
                dist = m.sqrt(distX ** 2 + distY ** 2)

                if dist < self.DISTANCE_CONSTRAINT:
                    d_v = Vector(distX, distY)
                    d_v.normalize_ip()

                    weight = -(self.DISTANCE_CONSTRAINT - dist) / self.DISTANCE_CONSTRAINT

                    self.danger_map.append((d_v, weight))
            else:
                self.danger_map.append((Vector(0, 0), 0))

    def combine(self, display):
        # Finds the danger closest to 0 (effectively the safest direction)
        max_danger_weight = max(self.danger_map, key=lambda v: v[1])
        danger_weights = []
        interest_weights = []
        # Mask any interest vectors whose corresponding danger vector has a higher weight
        for i in range(len(self.danger_map)):

            danger_weights.append(self.danger_map[i][1])
            # Compare danger vector length with the min danger vector
            if self.danger_map[i][1] < max_danger_weight[1]:
                self.masks[i] = False

        resultant_vector = Vector(0, 0)
        n = 0

        for j in range(len(self.interest_map)):
            interest_weights.append(self.interest_map[j][1])
            interest_vector = self.interest_map[j][0]
            if self.masks[j]:
                resultant_vector.x += interest_vector.x
                resultant_vector.y += interest_vector.y
                n += 1

        resultant_vector.x /= n
        resultant_vector.y /= n
        if resultant_vector.length() != 0:
            resultant_vector.normalize_ip()
        # Apply movement based on the combined interest direction
        self.x += resultant_vector.x * self.speed
        self.y += resultant_vector.y * self.speed
        print("Resultant vector:", resultant_vector)
        # Draw the resulting movement direction
        end_pos = (self.x + resultant_vector.x * 50, self.y + resultant_vector.y * 50)
        pygame.draw.line(display, (255, 255, 0), (self.x, self.y), end_pos, 2)

    def update(self, dangers, interests, display):
        self.pos = [self.x, self.y]
        self.avoid(dangers)
        self.chase(interests)
        self.combine(display)

    def draw(self, display):
        pygame.draw.circle(display, self.color, self.pos, 25)

    def draw_vectors(self, display):
        for vector, weight in self.interest_map:
            end_pos = (self.x + vector.x * 50, self.y + vector.y * 50)
            pygame.draw.line(display, (0, 255, 0), (self.x, self.y), end_pos, 2)
        for vector, weight in self.danger_map:
            end_pos = (self.x + vector.x * 50, self.y + vector.y * 50)
            pygame.draw.line(display, (255, 0, 0), (self.x, self.y), end_pos, 2)


acar = Entity(250, 250, (0, 0, 255))

car2 = Entity(150, 100, (0, 255, 0))
car3 = Entity(460, 100, (0, 255, 0))
car4 = Entity(100, 400, (0, 255, 0))

boundary = Entity(402, 100, (255, 0, 0))
boundary2 = Entity(120, 120, (255, 0, 0))
boundary3 = Entity(150, 380, (255, 0, 0))
screen = pygame.display.set_mode((500, 500))
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dangers = [boundary, boundary2, boundary3]
    interests = [car2, car3]
    acar.update(dangers, interests, screen)

    acar.draw(screen)

    for d in dangers:
        d.y -= 0.01
        d.update([], [], screen)
        d.draw(screen)
    for i in interests:
        i.y += 0.01
        i.draw(screen)
        i.update([], [], screen)
    acar.draw_vectors(screen)

    pygame.display.flip()
