import pygame
from math import *


class Player():
    def __init__(self):
        self.rect = pygame.Rect(50, 100, 50, 50)
        self.movement = pygame.Vector2(1, 0)
        self.speed = 5
        self.angle = 0

    def update(self, enemyvec):
        mx, my = pygame.mouse.get_pos()
        distY = my - 250
        hypotenuselength = sqrt((mx - 250) ** 2 + distY ** 2)

        self.angle = asin(distY/hypotenuselength)
        if mx < 250:
            self.angle = pi - self.angle

        self.movement.x = cos(self.angle)
        self.movement.y = sin(self.angle)

        self.rect.center = (200 * self.movement.x + 250, 200 * self.movement.y + 250)
        self.desirability = self.movement.dot(enemyvec)
        self.movement.normalize()


    def draw(self, surf):
        pygame.draw.line(surf, (0, 255, 0), (250, 250), self.rect.center, 2)
        pygame.draw.arc(surf, (255, 255, 255), pygame.Rect(225, 225, 50, 50), 0, -self.angle, 2)
