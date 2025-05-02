import pygame.draw

from chain import Chain
from util import parametric_equation_circle, Vector, lerp
import math as m


class Lizard:
    def __init__(self, distance):
        self.desired_distance = distance

        self.outline = []  # left side of animal
        self.other_side = []  # right side of animal

        self.bodysize = [52 // 2, 58 // 2, 40 // 2, 60 // 2, 68 // 2, 71 // 2, 65 // 2, 50 // 2, 28 // 2, 15 // 2,
                         11 // 2, 9 // 2, 7 // 2, 7 // 2]
        self.points = [(num * self.desired_distance, 250) for num in range(0, len(self.bodysize))]

        self.eye_closeness = 8

        self.spine = Chain((0, 250), 14, distance)
        self.speed = 5

        self.arms = []
        self.armsDesired = []
        for i in range(4):
            self.arms.append(Chain((0, 250), 3, 26 if i < 2 else 18))
            self.armsDesired.append(Vector(0, 0))

        self.outline = []
        self.other_side = []
        self.anchor = self.points[0]

        self.color = (82, 121, 111)

        self.stride = 100

    def resolve(self, screen, target):
        self.points[0] = target
        self.anchor = self.points[0]
        self.spine.resolve(target)
        i = 0
        for joint in self.arms:
            side = 1 if i % 2 == 0 else -1
            bodyIndex = 3 if i < 2 else 7
            angle = m.pi / 4 if i < 2 else m.pi / 3
            desired = Vector(self.getPosX(bodyIndex, angle * side, 80), self.getPosY(bodyIndex, angle * side, 40))
            if m.dist(desired, self.armsDesired[i]) > self.stride:
                self.armsDesired[i] = desired
            pygame.draw.circle(screen, (255, 0, 0), desired, 5)
            joint.fabrikResolve(Vector.lerp(Vector(self.arms[i].points[0][0], self.arms[i].points[0][1]),
                                            Vector(self.armsDesired[i][0], self.armsDesired[i][1]), 0.4), (
                                self.getPosX(bodyIndex, m.pi / 2 * side, -10),
                                self.getPosY(bodyIndex, m.pi / 2 * side, -10)))
            i += 1

    def update(self, screen, target, show_body_circles):
        global eye_right, eye_left
        quarter_turn = m.pi / 2
        self.resolve(screen, target)
        self.outline.clear()
        self.other_side.clear()
        for k, point in enumerate(self.spine.points):

            size = self.bodysize[k]
            theta = self.spine.angles[k]
            #   self.spine.angles[k] = theta
            if k == 0:
                smooth_f = 20
                self.other_side.append(parametric_equation_circle(-size, theta, point))
                for j in range(smooth_f // 2, 2, -1):
                    headleftpoint = parametric_equation_circle(-size, theta + m.pi / j, point)
                    headrightpoint = parametric_equation_circle(-size, theta - m.pi / j, point)
                    self.other_side.append(headleftpoint)
                    self.outline.append(headrightpoint)
                eye_left = parametric_equation_circle(size - self.eye_closeness, theta - quarter_turn, point)
                eye_right = parametric_equation_circle(size - self.eye_closeness, theta + quarter_turn, point)
            side_of_point = parametric_equation_circle(size, theta + quarter_turn,
                                                       self.spine.points[k])  # right side of animal

            other_side_of_point = parametric_equation_circle(size, theta - quarter_turn, self.spine.points[k])

            self.outline.append(side_of_point)
            self.other_side.append(other_side_of_point)
            if show_body_circles:
                pygame.draw.circle(screen, (255, 255, 255), point, self.bodysize[k], 2)

    def draw(self, screen):

        combined_points = self.other_side[::-1] + self.outline
        for i in range(len(self.arms)):

            shoulder = self.arms[i].points[2]
         #   pygame.draw.circle(screen, (0, 0, 255), shoulder, 5)
            shoulder = Vector(shoulder[0], shoulder[1])
            foot = self.arms[i].points[0]

            foot = Vector(foot[0], foot[1])
            elbow = self.arms[i].points[1]

          #  pygame.draw.circle(screen, (255, 0, 0), elbow, 5)

            elbow = Vector(elbow[0], elbow[1])

            para = Vector(foot.x - shoulder.x, foot.y - shoulder.y)
            perp = Vector(-para.y, para.x)
            perp.scale_to_length(30)
            if i == 2:
                elbow -= perp
            elif i == 3:
                elbow += perp
            self.arms[i].points[1] = (elbow.x, elbow.y)

            pygame.draw.circle(screen, self.color, foot, 10)
            pygame.draw.lines(screen, (255,255,255), False,
                              [(shoulder.x, shoulder.y), (elbow.x, elbow.y), (foot.x, foot.y)], 18)
            pygame.draw.lines(screen, self.color, False, [(shoulder.x, shoulder.y), (elbow.x,elbow.y), (foot.x, foot.y)], 16)

        #  for point in combined_points:
        #   pygame.draw.circle(screen, (255, 0, 0), point, 5)
        pygame.draw.polygon(screen, self.color, combined_points)
        pygame.draw.lines(screen, (255, 255, 255), True, combined_points, 2)
        pygame.draw.circle(screen, (255, 255, 255), eye_left, 6)
        pygame.draw.circle(screen, (255, 255, 255), eye_right, 6)

    def getPosX(self, i, angleOffset, lengthOffset):
        return self.spine.points[i][0] + m.cos(self.spine.angles[i] + angleOffset) * (self.bodysize[i] + lengthOffset)

    def getPosY(self, i, angleOffset, lengthOffset):
        return self.spine.points[i][1] + m.sin(self.spine.angles[i] + angleOffset) * (self.bodysize[i] + lengthOffset)
