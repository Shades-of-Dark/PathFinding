from chain import Chain
from util import Vector, parametric_equation_circle, cubic_bezier, draw_rotated_ellipse, relativeAngleDiff
import pygame
import math as m

WHITE = (255, 255, 255)


# lets make this lil guy
class Fish:

    def __init__(self, distance):
        self.body_color = (58, 124, 165)
        self.fin_color = (129, 195, 215)
        self.desired_distance = distance
        self.outline = []  # left side of animal
        self.other_side = []  # right side of animal

        self.bodysize = [34, 40, 42, 41, 38, 32, 25, 19, 16, 9]
        self.points = [(num * self.desired_distance, 250) for num in range(0, len(self.bodysize))]

        self.eye_closeness = 9

        self.spine = Chain((0, 250), 12, distance)

        self.cooltheta = 0
        self.head_reference_vector = Vector(1, 0)  # used to calculate head angle

        self.speed = 6  # how fast the animal moves

        oval_elongation = 2.5
        self.pec_fin_right = pygame.Rect(0, 0, 30, 30 * oval_elongation)
        self.pec_fin_left = pygame.Rect(0, 0, 30, 30 * oval_elongation)
        oval_elongation = 3
        self.ventral_fin_right = pygame.Rect(0, 0, 19, 19 * oval_elongation)
        self.ventral_fin_left = pygame.Rect(0, 0, 19, 19 * oval_elongation)
        dorsal_length = m.sqrt(
            (self.points[7][0] - self.points[4][0]) ** 2 + (self.points[7][1] - self.points[4][1]) ** 2)

        self.dorsal_fin_points = []

        self.show_rig = False
        self.headToTail = 0
        self.tail_theta = 0
        self.headToMid1 = 0
        self.headToMid2 = 0
        self.headToTail = 0
        self.old_value = 0

    def resolve(self, target):
        self.points[0] = target
        self.anchor = self.points[0]
        self.spine.resolve(target)

    #  self.spine.draw(screen)

    def update(self, screen, target, show_body_circles, line_width=2):
        global eye_right, eye_left

        self.headToMid1 = relativeAngleDiff(self.spine.angles[0], self.spine.angles[6])
        self.headToMid2 = relativeAngleDiff(self.spine.angles[0], self.spine.angles[7])
        self.headToTail = self.headToMid1 + relativeAngleDiff(self.spine.angles[6], self.spine.angles[-1])
        #   print(str(int(m.degrees(headToTail) * 5/18 + 0.5)) + "%")
        # print( + "%")
        #   print(tailWidth)

        self.outline.clear()
        self.other_side.clear()

        self.resolve(target)
        self.points = self.spine.points[:10]

        quarter_turn = m.pi / 2

        for k, point in enumerate(self.points):

            size = self.bodysize[k]
            if k == 0:
                #   dx_head = self.points[1][0] - self.points[0][0]
                # dy_head = self.points[1][1] - self.points[0][1]

                #    calc = Vector(dx_head, dy_head)
                #  calc = self.spine.apply_angle_constraint(calc, self.head_reference_vector)

                #   new_head_theta = m.atan2(calc.y, calc.x)

                self.head_theta = self.spine.angles[k]
                #     self.spine.joints[k] = calc
                #   self.spine.angles[k] = self.head_theta

                headtop = (size * -m.cos(self.head_theta) + point[0],
                           size * -m.sin(self.head_theta) + point[1])
                headleft = (size * -m.cos(self.head_theta + m.pi / 4) + point[0],
                            size * -m.sin(self.head_theta + m.pi / 4) + point[1])

                headright = (size * -m.cos(self.head_theta - m.pi / 4) + point[0],
                             size * -m.sin(self.head_theta - m.pi / 4) + point[1])
                headfullleft = (size * -m.cos(self.head_theta + quarter_turn) + point[0],
                                size * -m.sin(self.head_theta + quarter_turn) + point[1])
                headfullright = (size * -m.cos(self.head_theta - quarter_turn) + point[0],
                                 size * -m.sin(self.head_theta - quarter_turn) + point[1])

                eye_left = ((size - self.eye_closeness) * -m.cos(self.head_theta - quarter_turn) + point[0],
                            (size - self.eye_closeness) * -m.sin(self.head_theta - quarter_turn) + point[1])
                eye_right = ((size - self.eye_closeness) * -m.cos(self.head_theta + quarter_turn) + point[0],
                             (size - self.eye_closeness) * -m.sin(self.head_theta + quarter_turn) + point[1])

                self.other_side.append(headtop)  # tip of head
                self.other_side.append(headleft)
                self.other_side.append(headfullleft)

                self.outline.append(headright)
                self.outline.append(headfullright)

            #       pygame.draw.circle(screen, (255, 0, 0), headtop,
            #                line_width)
            #     pygame.draw.circle(screen, (255, 0, 0), headright,
            #                 line_width)
            #      pygame.draw.circle(screen, (255, 0, 0), headleft, line_width)
            #    pygame.draw.circle(screen, (255, 0, 0), headfullleft, line_width)

            #      pygame.draw.circle(screen, (255, 0, 0), headfullright, line_width)

            # if at the beginning, just add the head points
            elif k != 0:

                scaled_point = self.spine.points[k]
                theta = self.spine.angles[k]
                #   self.spine.angles[k] = theta

                side_of_point = parametric_equation_circle(size, theta + quarter_turn,
                                                           scaled_point)  # right side of animal

                other_side_of_point = parametric_equation_circle(size, theta - quarter_turn, scaled_point)  # left side
                # Calculate pectoral fins

                if k == 1:
                    self.head_reference_vector = self.spine.joints[
                        1]  # ensures we have a vector to calculate the head off of

                elif k == 3:
                    self.pec_fin_left.center = side_of_point
                    self.pec_fin_right.center = other_side_of_point

                # Calculate ventral fins
                elif k == 7:

                    self.ventral_fin_left.center = side_of_point
                    self.ventral_fin_right.center = other_side_of_point

                #     pygame.draw.circle(screen, (255, 0, 0), side_of_point, line_width)
                #      pygame.draw.circle(screen, (255, 0, 0), other_side_of_point, line_width)

                self.outline.append(side_of_point)
                self.other_side.append(other_side_of_point)

                if k == len(self.points) - 1:
                    self.tail_theta = theta
                    self.outline.append((size * -m.cos(theta + quarter_turn * 2.25) + scaled_point[0],
                                         size * -m.sin(theta + quarter_turn * 2.25) + scaled_point[
                                             1]))
                    self.outline.append((size * -m.cos(theta + quarter_turn * 2) + scaled_point[0],
                                         size * -m.sin(theta + quarter_turn * 2) + scaled_point[
                                             1]))  # add the tail point
                    self.other_side.append((size * -m.cos(theta + quarter_turn * 1.75) + scaled_point[0],
                                            size * -m.sin(theta + quarter_turn * 1.75) + scaled_point[
                                                1]))
                #  pygame.draw.circle(screen, (255, 0, 0), (size * m.cos(theta + quarter_turn * 2) + scaled_point[0],
                #                           size * m.sin(theta + quarter_turn * 2) + scaled_point[1]),
                #   line_width)

            if show_body_circles:
                self.show_rig = True
                pygame.draw.circle(screen, WHITE, point, size, 5)  # body segment visiualisation

        if show_body_circles:
            pygame.draw.lines(screen, WHITE, False, self.points, 5)  # IF YOU WANT TO SEE SPINAL COORD

    def draw(self, screen):

        combined_points = self.other_side[::-1] + self.outline  # just adds the head to put it all together

        if not self.show_rig:

            tilt = 60  # how far back the fins tilt

            # PECTORAL FINS DRAWING STARTS HERE
            draw_rotated_ellipse(screen, self.fin_color, self.pec_fin_left, -m.degrees(self.spine.angles[2]) + tilt)
            draw_rotated_ellipse(screen, WHITE, self.pec_fin_left, -m.degrees(self.spine.angles[2]) + tilt, 2)

            draw_rotated_ellipse(screen, self.fin_color, self.pec_fin_right, -m.degrees(self.spine.angles[2]) - tilt)
            draw_rotated_ellipse(screen, WHITE, self.pec_fin_right, -m.degrees(self.spine.angles[2]) - tilt,
                                 2)

            # PECTORAL FINS DRAWING ENDS HERE
            tilt = 45
            # VENTRAL FINS DRAWING STARTS HERE

            draw_rotated_ellipse(screen, self.fin_color, self.ventral_fin_left,
                                 -m.degrees(self.spine.angles[6]) + tilt)
            draw_rotated_ellipse(screen, WHITE, self.ventral_fin_left,
                                 -m.degrees(self.spine.angles[6]) + tilt,
                                 2)

            draw_rotated_ellipse(screen, self.fin_color, self.ventral_fin_right,
                                 -m.degrees(self.spine.angles[6]) - tilt)
            draw_rotated_ellipse(screen, WHITE, self.ventral_fin_right,
                                 -m.degrees(self.spine.angles[6]) - tilt, 2)

            # VENTRAL FINS DRAWING ENDS HERE
            pygame.draw.polygon(screen, self.body_color, combined_points)

            # DORSAL FIN DRAWING STARTS HERE
            # Rooted endpoints
            start_point = self.points[6]  # Fixed starting endpoint
            end_point = self.points[3]  # Fixed ending endpoint

            # Measure curvature for the control points
            fish_curve_direction = self.old_value + (
                    -m.copysign(1, self.spine.angles[6] - self.spine.angles[3]) - self.old_value) * 0.1
            self.old_value = fish_curve_direction
            # Adjust the middle control points to curve opposite the fish's curvature
            c_f = 12
            control_point1 = (
                start_point[0] + m.cos(self.spine.angles[6] + fish_curve_direction * m.pi / 2) * self.headToMid2 * c_f,
                start_point[1] + m.sin(self.spine.angles[6] + fish_curve_direction * m.pi / 2) * self.headToMid2 * c_f,
            )
            control_point2 = (
                end_point[0] + m.cos(self.spine.angles[3] + fish_curve_direction * m.pi / 2) * self.headToMid1 * c_f,
                end_point[1] + m.sin(self.spine.angles[3] + fish_curve_direction * m.pi / 2) * self.headToMid1 * c_f,
            )

            bezier_points = [self.spine.points[3]]
            # Draw the cubic Bezier curve for the dorsal fin
            last_bezier = start_point  # Start of the curve
            for i in range(101):  # Interpolating the curve
                t = i / 100
                bezier_point = (
                    (1 - t) ** 3 * start_point[0] + 3 * (1 - t) ** 2 * t * control_point1[0] +
                    3 * (1 - t) * t ** 2 * control_point2[0] + t ** 3 * end_point[0],
                    (1 - t) ** 3 * start_point[1] + 3 * (1 - t) ** 2 * t * control_point1[1] +
                    3 * (1 - t) * t ** 2 * control_point2[1] + t ** 3 * end_point[1],
                )
                pygame.draw.line(screen, WHITE, last_bezier, bezier_point, 4)
                last_bezier = bezier_point
                bezier_points.append(bezier_point)
            bezier_points.append(self.spine.points[6])
            pygame.draw.polygon(screen, self.fin_color, bezier_points)
            pygame.draw.line(screen, WHITE, bezier_points[0], bezier_points[-1])
            # DORSAL FIN DRAWING ENDS HERE

            pygame.draw.circle(screen, WHITE, eye_left, 6)
            pygame.draw.circle(screen, WHITE, eye_right, 6)

            # CAUDAL FIN DRAWING STARTS HERE
            caudal_fin_points = []
            for i in range(8, 11):
                tailWidth = 1.5 * self.headToTail * (i - 8) * (i - 8)
                caudal_fin_points.append((self.spine.points[i][0] + m.cos(self.spine.angles[i] - m.pi / 2) * tailWidth,
                                          self.spine.points[i][1] + m.sin(self.spine.angles[i] - m.pi / 2) * tailWidth))
            for i in range(11, 8, -1):
                tailWidth = max(-13, min(13, self.headToTail * 6))
                caudal_fin_points.append((self.spine.points[i][0] + m.cos(self.spine.angles[i] + m.pi / 2) * tailWidth,
                                          self.spine.points[i][1] + m.sin(self.spine.angles[i] + m.pi / 2) * tailWidth))
            pygame.draw.polygon(screen, self.fin_color, caudal_fin_points)
            pygame.draw.lines(screen, WHITE, True, caudal_fin_points, 2)
        #  pygame.draw.line(screen, WHITE, self.spine.points[8], self.spine.points[11], 3)
        # CAUDAL FIN DRAWING ENDS HERE
        else:
            for point in self.outline:
                pygame.draw.circle(screen, (0, 255, 0), point, 4)  # Green for left side
            for point in self.other_side:
                pygame.draw.circle(screen, (255, 0, 0), point, 4)  # Red for right side

        pygame.draw.lines(screen, WHITE, True, combined_points, 2)
