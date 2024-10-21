import pygame


class Enemy():
    def __init__(self):
        self.rect = pygame.Rect(225, 225, 50, 50)
        self.movement = pygame.Vector2(1, 0)


    def update(self):
        pass

    def draw(self, surf):
        pygame.draw.line(surf, (255, 0, 0), (250, 250), (450, 250), 2)
