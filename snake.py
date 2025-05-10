from chain import Chain, Vector
import pygame
import math as m

WHITE = (255, 255, 255)


class Snake():

    def __init__(self, origin):
        self.body_color = (172, 57, 49)

        self.outline = []  # left side of animal
        self.other_side = []  # right side of animal

        self.bodysize = [40, 45, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 32, 30, 28, 28, 28, 28, 28, 28, 28, 28, 28,
                         26, 26, 24, 22, 21, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 7, 7, 7, 7, 7, 5]  # snake body

        self.eye_closeness = 15

        self.spine = Chain((0, 250), len(self.bodysize), 32)
        self.cooltheta = 0
        self.head_reference_vector = Vector(1, 0)  # used to calculate head angle

        self.speed = 4  # how fast the animal moves
        self.show_rig = False

    def update(self, screen, target, show_body_circles, line_width=2):
        global eye_right, eye_left


        self.outline.clear()
        self.other_side.clear()
        self.spine.resolve(target)

        quarter_turn = m.pi / 2

        for k, point in enumerate(self.spine.points):
            size = self.bodysize[k]
            theta = self.spine.angles[k]
            if k == 0:

                headtop = (size * -m.cos(theta) + point[0],
                           size * -m.sin(theta) + point[1])
                headleft = (size * -m.cos(theta + m.pi / 4) + point[0],
                            size * -m.sin(theta + m.pi / 4) + point[1])
                headright = (size * -m.cos(theta - m.pi / 4) + point[0],
                             size * -m.sin(theta - m.pi / 4) + point[1])
                headfullleft = (size * -m.cos(theta + quarter_turn) + point[0],
                                size * -m.sin(theta + quarter_turn) + point[1])
                headfullright = (size * -m.cos(theta - quarter_turn) + point[0],
                                 size * -m.sin(theta - quarter_turn) + point[1])

                eye_left = ((size - self.eye_closeness) * -m.cos(theta - quarter_turn) + point[0],
                            (size - self.eye_closeness) * -m.sin(theta - quarter_turn) + point[1])
                eye_right = ((size - self.eye_closeness) * -m.cos(theta + quarter_turn) + point[0],
                             (size - self.eye_closeness) * -m.sin(theta + quarter_turn) + point[1])
                self.other_side.extend([headtop, headleft, headfullleft])

                self.outline.extend([headright, headfullright])

                # pygame.draw.circle(screen, (255, 0, 0), headtop,
                #                   line_width)
                # pygame.draw.circle(screen, (255, 0, 0), headright,
                #                  line_width)
                # pygame.draw.circle(screen, (255, 0, 0), headleft, line_width)
                # pygame.draw.circle(screen, (255, 0, 0), headfullleft, line_width)

                # pygame.draw.circle(screen, (255, 0, 0), headfullright, line_width)

                # if at the beginning, just add the head points
            elif k != 0:

                side_of_point = (size * m.cos(theta + quarter_turn) + point[0],
                                 size * m.sin(theta + quarter_turn) + point[1])  # right side of animal

                other_side_of_point = (size * m.cos(theta - quarter_turn) + point[0],  # left side of animal
                                       size * m.sin(theta - quarter_turn) + point[

                                           1])  # right side of animal

                # pygame.draw.circle(screen, (255, 0, 0), side_of_point, line_width)
                # pygame.draw.circle(screen, (255, 0, 0), other_side_of_point, line_width)

                self.outline.append(side_of_point)
                self.other_side.append(other_side_of_point)

                if k == len(self.spine.points) - 1:
                    self.outline.append((size * -m.cos(theta + quarter_turn * 2.25) + point[0],
                                         size * -m.sin(theta + quarter_turn * 2.25) + point[
                                             1]))
                    self.outline.append((size * -m.cos(theta + quarter_turn * 2) + point[0],
                                         size * -m.sin(theta + quarter_turn * 2) + point[
                                             1]))  # add the tail point

                    self.other_side.append((size * -m.cos(theta + quarter_turn * 1.75) + point[0],
                                            size * -m.sin(theta + quarter_turn * 1.75) + point[
                                                1]))
            #       pygame.draw.circle(screen, (255, 0, 0), (size * m.cos(theta + quarter_turn * 2) + point[0],
            #                       size * m.sin(theta + quarter_turn * 2) + point[1]),
            #    line_width)

            if show_body_circles:
                self.show_rig = True
                pygame.draw.circle(screen, WHITE, point, size, 5)  # body segment visiualisation
                pygame.draw.lines(screen, WHITE, False, self.spine.points, 5)  # IF YOU WANT TO SEE SPINAL COORD

    def draw(self, screen):
        combined_points = self.other_side[::-1] + self.outline  # just adds the head to put it all together

        if not self.show_rig:

            pygame.draw.polygon(screen, self.body_color, combined_points)
            pygame.draw.circle(screen, WHITE, eye_left, 8)
            pygame.draw.circle(screen, WHITE, eye_right, 8)
        else:
            for point in self.outline:
                pygame.draw.circle(screen, (0, 255, 0), point, 4)  # Green for outline
            for point in self.other_side:
                pygame.draw.circle(screen, (255, 0, 0), point, 4)  # Red for other side
        pygame.draw.lines(screen, WHITE, False, combined_points)
