import pygame
import math as m
from util import Vector




WHITE = (255, 255, 255)


# distance is just the link size between each joint
class Chain:
    def __init__(self, origin, joint_count, linksize, angle_constr=m.pi/8):
        self.head_theta = 0
        self.desired_distance = linksize
        self.points = [(linksize * x + origin[0], origin[1]) for x in range(joint_count)]

        self.anchor = self.points[0]
        self.cooltheta = 0
        self.angle_constraint = angle_constr
        self.sec_ang_constraint = 2 * m.pi - angle_constr
        self.head_reference_vector = Vector(1, 0)  # used to calculate head angle
        self.angles = [i for i in range(joint_count)]  # some initialization stuff
        self.joints = [Vector(k, 0) for k in range(joint_count)]  # some init stuff

    def constrain_distance(self, pos, anchor, constraint):
        new_vector =  anchor + anchor-pos
        new_vector.xy = new_vector.x/new_vector.length(), new_vector.y/new_vector.length()
        return new_vector * constraint

    def apply_angle_constraint(self, calc: Vector, other: Vector):
        current_angle = calc.normalize_angle(
            calc.angle_to(other))  # Get current angle of the vector

        if self.angle_constraint < m.radians(current_angle) < m.pi:  # clockwise rotation snapping
            return calc.rotate_rad(m.radians(current_angle) - self.angle_constraint)
        elif m.pi < m.radians(current_angle) < self.sec_ang_constraint:  # counterclockwise rotation snapping

            return calc.rotate_rad(m.radians(current_angle) - self.sec_ang_constraint)
        else:
            return calc

    def update(self, target):
        self.resolve(target)

    def draw(self, screen):
        pygame.draw.lines(screen, WHITE, False, self.points, 5)  # IF YOU WANT TO SEE SPINAL COORD

    def fabrikResolve(self, pos, anchor):
        self.points[0] = pos
        for i in range(1, len(self.points)):
            self.joints[i] = self.constrain_distance(self.joints[i], self.joints[i-1], self.desired_distance)
            test_vector = self.joints[i].normalize()
            self.points[i] = self.points[0][0] + self.desired_distance * test_vector.x, self.points[0][1] + self.desired_distance * test_vector.y
        self.points[-1] = anchor  # anchors the arm
        for i in range(len(self.points)-2, 0, -1):
            self.joints[i] = self.constrain_distance(self.joints[i], self.joints[i + 1], self.desired_distance)
            test_vector = self.joints[i].normalize()
            self.points[i] = anchor[0] + self.desired_distance * test_vector.x, anchor[
                1] + self.desired_distance * test_vector.y



    def resolve(self, target):

        self.points[0] = target
        self.anchor = self.points[0]

        for k, point in enumerate(self.points):

            if k == 0:
                dx_head = self.points[1][0] - self.points[0][0]
                dy_head = self.points[1][1] - self.points[0][1]

                calc = Vector(dx_head, dy_head)
                calc = self.apply_angle_constraint(calc, self.head_reference_vector)

                new_head_theta = m.atan2(calc.y, calc.x)

                self.head_theta = new_head_theta
                self.joints[k] = calc
                self.angles[k] = self.head_theta



            #       pygame.draw.circle(screen, (255, 0, 0), headtop,
            #                line_width)
            #     pygame.draw.circle(screen, (255, 0, 0), headright,
            #                 line_width)
            #      pygame.draw.circle(screen, (255, 0, 0), headleft, line_width)
            #    pygame.draw.circle(screen, (255, 0, 0), headfullleft, line_width)

            #      pygame.draw.circle(screen, (255, 0, 0), headfullright, line_width)

            # if at the beginning, just add the head points
            elif k != 0:

                dx, dy = point[0] - self.anchor[0], point[1] - self.anchor[1]
                calc = Vector(dx, dy)

                #  print("Snapped otherway")
                dx_norm, dy_norm = dx / calc.magnitude(), dy / calc.magnitude()

                calc.xy = dx_norm, dy_norm

                calc = self.apply_angle_constraint(calc, self.joints[k - 1])

                scaled_dx = self.desired_distance * calc.x
                scaled_dy = self.desired_distance * calc.y
                scaled_point = (self.anchor[0] + scaled_dx, self.anchor[1] + scaled_dy)

                self.points[k] = scaled_point
                self.anchor = scaled_point

                self.joints[k] = calc
                new_theta = m.atan2(calc.y, calc.x)

                delta_theta = new_theta - self.cooltheta
                self.cooltheta += delta_theta
                theta = self.cooltheta
                self.angles[k] = theta
                #   self.spine.angles[k] = theta

                if k == 1:
                    self.head_reference_vector = calc  # ensures we have a vector to calculate the head off of
