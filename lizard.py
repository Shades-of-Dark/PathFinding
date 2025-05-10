import pygame.draw

from chain import Chain
from util import parametric_equation_circle, Vector, lerp
import math as m

WHITE = (255, 255, 255)


class Lizard:
    def __init__(self, distance):
        self.desired_distance = distance
        # Add a leg length multiplier parameter to easily adjust leg length

        self.outline = []  # left side of animal
        self.other_side = []  # right side of animal
        s = 2
        self.bodysize = [52 / s, 58 / s, 40 / s, 60 / s, 68 / s, 71 / s, 65 / s, 50 / s, 28 / s, 15 / s,
                         11 / s, 9 / s, 7 / s, 7 / s]
        self.points = [(num * self.desired_distance, 250) for num in range(0, len(self.bodysize))]

        self.eye_closeness = 8

        self.spine = Chain((500, 250), 14, distance)
        self.speed = 5

        # Define base leg lengths
        self.front_leg_length = 39
        self.back_leg_length = 27

        # You can also adjust the number of segments for more complex leg movement
        self.leg_segments = 3

        self.arms = []
        self.armsDesired = []
        for i in range(4):
            # Use the adjusted leg lengths
            segment_length = self.front_leg_length if i < 2 else self.back_leg_length
            self.arms.append(Chain((500, 250), self.leg_segments, segment_length))

            self.armsDesired.append(Vector(0, 0))

        self.outline = []
        self.other_side = []
        self.anchor = self.points[0]

        self.color = (82, 121, 111)

        # Adjust stride based on leg length
        self.stride = 200

    def resolve(self, screen, target):
        self.points[0] = target
        self.anchor = self.points[0]
        self.spine.resolve(target)
        i = 0

        for joint in self.arms:
            side = 1 if i % 2 == 0 else -1
            bodyIndex = 3 if i < 2 else 6
            angle = m.pi/2 if i < 2 else m.pi / 3
            joint_offset = 0 if i<2 else -5
            foot_offset = 40
            desiredIndex = 0 if i <2 else 5
            # Adjust the leg position offset based on leg length

            desired = Vector(self.getPosX(desiredIndex, angle * side, foot_offset),
                             self.getPosY(desiredIndex, angle * side, foot_offset))

            if m.dist(desired.xy, self.armsDesired[i].xy) > self.stride:
                self.armsDesired[i] = desired
            # DEBUG STUFF -------------------
            # pygame.draw.circle(screen, (0, 0, 255), desired.xy, 8, 3)
            #    pygame.draw.circle(screen, (0, 255, 0), self.armsDesired[i].xy, 8)
            #pygame.draw.circle(screen, (0, 255, 0), self.armsDesired[i], 8, 3)
            #  pygame.draw.circle(screen, (0, 255, 0), desired, 5)
            # ----------------------------------------------
            joint.fabrikResolve(Vector.lerp(Vector(self.arms[i].points[0][0], self.arms[i].points[0][1]),
                                            self.armsDesired[i], 0.4), (
                                    self.getPosX(bodyIndex, (m.pi / 2) * side, joint_offset),
                                    self.getPosY(bodyIndex, (m.pi / 2) * side, joint_offset)))
            i += 1

    def update(self, screen, target, show_body_circles):
        global eye_right, eye_left
        quarter_turn = m.pi / 2
        self.resolve(screen, target)
        self.outline.clear()
        self.other_side.clear()
        self.points = self.spine.points
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
                pygame.draw.circle(screen, WHITE, point, self.bodysize[k], 2)

    def draw(self, screen):
        # Draw the limbs as rounded appendages

        for i in range(len(self.arms)):

            # Get positions from the chain
            shoulder = self.arms[i].points[2]
            foot = self.arms[i].points[0]
            elbow = self.arms[i].points[1]
            # Convert to vectors for easier manipulation

            # Store the calculated elbow position back to the chain
            para = Vector(foot[0], foot[1]) - Vector(shoulder[0], shoulder[1])
            perp = Vector(-para.y, para.x)

            perp.scale_to_length(30)
            elbow_vec = Vector(elbow[0], elbow[1])
            if i == 2:
                elbow_vec = elbow_vec - perp
            elif i == 3:
                elbow_vec = elbow_vec + perp
            # Draw the limb segments
            w = 3
            points = [shoulder, elbow_vec.xy, foot]

            pygame.draw.lines(screen, WHITE, False, points, 19)

            pygame.draw.lines(screen, self.color, False, points, 16)
            # DEBUG VISUALISATION ----------
            # pygame.draw.circle(screen, WHITE, points[1], 8, 3)
            # pygame.draw.circle(screen, WHITE, points[2], 8, 3)
            # pygame.draw.circle(screen, WHITE, points[0], 8, 3)

            # pygame.draw.line(screen, WHITE, points[0], points[1], 3)
            # pygame.draw.line(screen, (255, 0, 255), points[1], points[2], 3)
            # -------------------------------------------------

        # Draw the body
        combined_points = self.other_side[::-1] + self.outline
        pygame.draw.polygon(screen, self.color, combined_points)
        pygame.draw.lines(screen, WHITE, True, combined_points, 2)

        # Draw the eyes
        pygame.draw.circle(screen, WHITE, eye_left, 6)
        pygame.draw.circle(screen, WHITE, eye_right, 6)

    def getPosX(self, i, angleOffset, lengthOffset):
        return self.spine.points[i][0] + m.cos(self.spine.angles[i] + angleOffset) * (self.bodysize[i] + lengthOffset)

    def getPosY(self, i, angleOffset, lengthOffset):
        return self.spine.points[i][1] + m.sin(self.spine.angles[i] + angleOffset) * (self.bodysize[i] + lengthOffset)
