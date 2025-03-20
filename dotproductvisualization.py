import sys

import pygame
from math import *

sys.path.insert(0, '..')
from pixelartfontsystem.pixelfont import *

pygame.init()

screen = pygame.display.set_mode((500, 500), 0, 32)

clock = pygame.time.Clock()
font = Font("font.png")


class Enemy():
    def __init__(self):
        self.rect = pygame.Rect(225, 225, 50, 50)
        self.movement = pygame.Vector2(1, 0)

    def update(self):
        pass

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 255, 255), (450, 250), 8)
        pygame.draw.line(surf, (255, 0, 0), (250, 250), (450, 250), 4)


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

        self.angle = asin(distY / hypotenuselength)
        if mx < 250:
            self.angle = pi - self.angle

        self.movement.x = cos(self.angle)
        self.movement.y = sin(self.angle)
        self.movement.normalize_ip()
        self.rect.center = (200 * self.movement.x + 250, 200 * self.movement.y + 250)
        self.desirability = self.movement.dot(enemyvec)
        self.movement.normalize()

    def draw(self, surf):
        pygame.draw.line(surf, (0, 255, 0), (250, 250), self.rect.center, 4)
        pygame.draw.circle(surf, (255, 255, 255), self.rect.center, 8)

        pygame.draw.arc(surf, (255, 255, 255), pygame.Rect(225, 225, 50, 50), 0, -self.angle, 2)
        pygame.draw.line(surf, (255, 255, 255), (450, 250), self.rect.center, 3)


pygame.display.set_caption("Dot Product Visualization")

goodGuy = Player()
badGuy = Enemy()
circle_radius = 200
k_board = str(0)
while True:
    screen.fill((0, 0, 0))

    goodGuy.update(badGuy.movement)
    badGuy.update()

    for event in pygame.event.get():
        pygame.event.pump()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.unicode.isnumeric():
                k_board += event.unicode
            elif event.unicode == "\r":
                k_board = "0"
    if int(k_board) != 0:
        angle = int(k_board)
    else:
        angle = goodGuy.movement.angle_to(badGuy.movement)
    font.render(screen, "DOT: " + str(round(goodGuy.desirability, 2)), (255, 255, 255), (200, 270), 4, (0, 0, 0), False)
    font.render(screen, "Angle: " + str(round(angle)), (255, 255, 255), (20, 10), 4, (0, 0, 0), False)
    font.render(screen, f"({round(cos(angle % 360) * circle_radius, 1)}, {round(sin(angle % 360) * circle_radius, 1)})", (255, 255, 255), (310, 10), 3, (0, 0, 0), False)
    goodGuy.draw(screen)
    badGuy.draw(screen)

    pygame.draw.circle(screen, (255, 255, 255), (250, 250), circle_radius, 4)
    pygame.draw.circle(screen, (255, 255, 255), (250, 250), 8)

    pygame.display.flip()
    clock.tick(60)
