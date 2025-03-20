import pygame.draw

from chain import Chain
from util import parametric_equation_circle, Vector
import math as m


class Lizard:
    def __init__(self, distance):
        self.desired_distance = distance

        self.outline = []  # left side of animal
        self.other_side = []  # right side of animal

        self.bodysize = [52 // 2, 58 // 2, 40 // 2, 60 // 2, 68 // 2, 71 // 2, 65 // 2, 50 // 2, 28 // 2, 15 // 2,
                         11 // 2, 9 // 2, 7 // 2, 7 // 2]
        self.points = [(num * self.desired_distance, 250) for num in range(0, len(self.bodysize))]

        self.eye_closeness = 9

        self.spine = Chain((0, 250), 14, distance)
        self.speed = 5

        self.arms = []
        self.armsDesired = []
        for i in range(4):
            self.arms.append(Chain((0, 250), 3, 5))
            self.armsDesired.append(Vector(0, 0))

        self.outline = []
        self.other_side = []
        self.anchor = self.points[0]

    def resolve(self, target):
        self.points[0] = target
        self.anchor = self.points[0]
        self.spine.resolve(target)
        for joint in self.arms:
            joint.fabrikResolve(target, self.spine.points[4])

    def update(self, screen, target, show_body_circles):
        quarter_turn = m.pi / 2
        self.resolve(target)
        self.outline.clear()
        self.other_side.clear()
        for k, point in enumerate(self.spine.points):
            size = self.bodysize[k]
            theta = self.spine.angles[k]
            #   self.spine.angles[k] = theta

            side_of_point = parametric_equation_circle(size, theta + quarter_turn,
                                                       self.spine.points[k])  # right side of animal

            other_side_of_point = parametric_equation_circle(size, theta - quarter_turn, self.spine.points[k])

            self.outline.append(side_of_point)
            self.other_side.append(other_side_of_point)
            if k == 4:
                arm_side_point = parametric_equation_circle(10, theta + quarter_turn, self.arms[0].points[1])
                arm_other_side_point = parametric_equation_circle(10, theta - quarter_turn, self.arms[0].points[1])
                self.outline.append(arm_side_point)
                self.other_side.append(arm_other_side_point)

    def draw(self, screen):
        combined_points = self.other_side[::-1] + self.outline  # just adds the head to put it all together

        pygame.draw.polygon(screen, (0, 120, 0), combined_points)
        pygame.draw.lines(screen, (255, 255, 255), True, combined_points, 2)
