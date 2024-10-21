import sys

import pygame

from enemy import Enemy
from player import Player

sys.path.insert(0, '..')
from pixelartfontsystem.pixelfont import *

pygame.init()

screen = pygame.display.set_mode((500, 500), 0, 32)

clock = pygame.time.Clock()
font = Font("font.png")

goodGuy = Player()
badGuy = Enemy()
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        pygame.event.pump()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    goodGuy.update(badGuy.movement)
    badGuy.update()
    font.render(screen, "DOT: " + str(round(goodGuy.desirability, 2)), (255, 255, 255), (200, 270), 4, (0, 0, 0), False)

    goodGuy.draw(screen)
    badGuy.draw(screen)
    pygame.draw.circle(screen, (255,255,255), (250, 250), 200, 2)
    pygame.display.flip()
    clock.tick(60)
