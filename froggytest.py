import sys

import pygame
from frog import Frog
from util import Vector
pygame.display.set_caption("Froggy Test")

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()
froggy = Frog((screen.get_width()//2, screen.get_height()//2))

while True:
    clock.tick(60)
    screen.fill((40, 44, 52))
    click = pygame.mouse.get_pressed(3)[0]
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    froggy.draw(screen)
    froggy.update(mx, my, click)
    pygame.display.update()