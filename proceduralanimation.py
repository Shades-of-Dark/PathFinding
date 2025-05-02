import sys
from snake import Snake
from fish import Fish
from lizard import Lizard
import pygame
import math as m

# parametric equation for body sides,

#      pygame.draw.circle(screen, WHITE, point, desired_distance, 2)  # distance constraint visualization


pygame.display.set_caption("Procedural Animation")

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WHITE = (255, 255, 255)
desired_distance = 32

snake = Snake(desired_distance)
lizard = Lizard(desired_distance)
fish = Fish(desired_distance)  # fish color:
clock = pygame.time.Clock()

p = 0


current_body = snake
while True:
    screen.fill((40, 44, 52))
    mx, my = pygame.mouse.get_pos()
    leftclick = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                desired_distance += 10
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_s:
                current_body = snake
            elif event.key == pygame.K_f:
                current_body = fish
            elif event.key == pygame.K_l:
                current_body = lizard

    # fluid_movement = (p * 80 + m.sin(p * 0.1) * 90, m.sin(p) * 80 + 400)
    # p += 0.08

    # surface, target, vertice display, body segments
    move_slowly = m.atan2(my - current_body.points[0][1], mx - current_body.points[0][0])
    move_towards_target = (
        m.cos(move_slowly) * current_body.speed + current_body.points[0][0],
        m.sin(move_slowly) * current_body.speed + current_body.points[0][1])
    current_body.show_rig = leftclick[0]
    current_body.update(screen, move_towards_target, leftclick[2])
    current_body.desired_distance = desired_distance

 #   current_body.spine.update(screen, move_towards_target, show_body_circles=False) # view spine
    current_body.draw(screen)
    pygame.display.update()
    clock.tick(60)
