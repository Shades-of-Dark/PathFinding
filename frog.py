import math
import pygame
import pygame.draw
import math as m
from blob import Blob, BlobPoint
from util import heading, draw_rotated_ellipse, lerp, Vector, generate_spline_points
from limb import Limb

WIDTH, HEIGHT = 1920, 1080


def bezier_curve(surface, color, start_point, control1, control2, end_point, width=1, steps=50):
    """
    Draw a bezier curve like Processing's bezierVertex

    Args:
        surface: pygame surface to draw on
        color: color tuple (r, g, b)
        start_point: tuple (x, y) - starting point
        control1: tuple (x, y) - first control point
        control2: tuple (x, y) - second control point
        end_point: tuple (x, y) - ending point
        width: line width (default 1)
        steps: number of steps for curve smoothness (default 50)
    """
    points = []

    for i in range(steps + 1):
        t = i / steps

        # Cubic bezier formula: B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
        x = (1 - t) ** 3 * start_point[0] + 3 * (1 - t) ** 2 * t * control1[0] + 3 * (1 - t) * t ** 2 * control2[
            0] + t ** 3 * end_point[0]
        y = (1 - t) ** 3 * start_point[1] + 3 * (1 - t) ** 2 * t * control1[1] + 3 * (1 - t) * t ** 2 * control2[
            1] + t ** 3 * end_point[1]

        points.append((int(x), int(y)))

    if len(points) > 1:
        pygame.draw.lines(surface, color, False, points, width)

    return points


def draw_front_leg(surf, anchor: Vector, limb: Limb):
    # Draw as simple segmented lines: anchor -> elbow -> foot
    spline_points = generate_spline_points([BlobPoint(anchor), limb.elbow, limb.foot], resolution=15)

    point_tuples = [(int(p.x), int(p.y)) for p in spline_points]
    point_tuples = point_tuples[:31]

    pygame.draw.lines(surf, (0,0,0),False, point_tuples, 48)
    pygame.draw.lines(surf, (85, 145, 127), False, point_tuples, 34)


class Frog():
    def __init__(self, origin):
        self.blob = Blob(origin, 16, 128, 1.5)

        # Improved limb initialization with better angles and positioning
        self.leftFrontLeg = Limb((origin[0] - 60, origin[1]), 56, 7 * m.pi / 4, 15 * m.pi / 8, 9 * m.pi / 5, m.pi / 4)
        self.rightFrontLeg = Limb((origin[0] + 60, origin[1]), 56, 7 * m.pi / 4, m.pi / 8, 9 * m.pi / 5, 7 * m.pi / 4)

        self.leftHindLeg = Limb((origin[0] - 80, origin[1] + 20), 100, m.pi * 8.1 / 5, 6 * m.pi / 5, 8 * m.pi / 5,
                                2 * m.pi / 5)
        self.rightHindLeg = Limb((origin[0] + 80, origin[1] + 20), 100, m.pi * 8.1/ 5, 2 * m.pi / 5, 8 * m.pi / 5,
                                 8 * m.pi / 5)

        # Ground detection and movement variables
        self.ground_level = HEIGHT - 10
        self.left_hind_grounded = False
        self.right_hind_grounded = False
        self.step_cycle = 0
        self.step_speed = 0.02

        self.headW, self.headH = 250, 225
        self.headSurf = pygame.Surface((self.headW + 64, self.headH + 64))
        self.headSurf.fill((255, 255, 255))
        self.headSurf.set_colorkey((255, 255, 255))

        # Center offset for drawing
        cx, cy = (self.headW + 64) // 2, (self.headH + 64) // 2

        # Head outline - make rect larger to accommodate full 8px outline thickness
        # Processing: arc(0, 75, 250, 225, -PI, 0) - from -PI to 0 (top half)

        head_outline_rect = pygame.Rect(cx - self.headW // 2 - 8, cy - self.headH // 2 + 75 - 8, self.headW + 16,
                                        self.headH + 16)
        pygame.draw.arc(self.headSurf, (0, 0, 0), head_outline_rect, 2 * m.pi, m.pi, 8)

        # Head fill (ellipse from Processing: ellipse(0, 75, 244, 219))
        head_fill_rect = pygame.Rect(cx - 122, cy - 110 + 75, 244, 219)
        pygame.draw.ellipse(self.headSurf, (85, 145, 127), head_fill_rect)

        # Eye socket arcs - expand rects to show full 8px thickness
        left_eye_socket = pygame.Rect(cx - 75 - 37 - 8, cy - 10 - 37 - 8, 75 + 16, 75 + 16)
        right_eye_socket = pygame.Rect(cx + 75 - 37 - 8, cy - 10 - 37 - 8, 75 + 16, 75 + 16)

        # Processing left: arc(-75, -10, 75, 75, -PI-PI/4.6, -PI/5.6)
        # Processing right: arc(75, -10, 75, 75, -PI+PI/5.6, PI/4.6)
        # Convert to pygame counter-clockwise angles
        pygame.draw.arc(self.headSurf, (0, 0, 0), left_eye_socket,
                        2 * m.pi + m.pi / 4.6, m.pi + m.pi / 5.6, 8)
        pygame.draw.arc(self.headSurf, (0, 0, 0), right_eye_socket, 2 * m.pi - m.pi / 5.6,
                        m.pi + -m.pi / 4.6, 8)

        # Eye sockets
        left_socket_fill = pygame.Rect(cx - 75 - 35, cy - 10 - 35, 70, 70)
        right_socket_fill = pygame.Rect(cx + 75 - 35, cy - 10 - 35, 70, 70)
        pygame.draw.ellipse(self.headSurf, (85, 145, 127), left_socket_fill)
        pygame.draw.ellipse(self.headSurf, (85, 145, 127), right_socket_fill)

        # Eyes
        left_eye = pygame.Rect(cx - 75 - 24, cy - 10 - 24, 48, 48)
        right_eye = pygame.Rect(cx + 75 - 24, cy - 10 - 24, 48, 48)
        pygame.draw.ellipse(self.headSurf, (0, 0, 0), left_eye, 4)
        pygame.draw.ellipse(self.headSurf, (0, 0, 0), right_eye, 4)
        pygame.draw.ellipse(self.headSurf, (240, 153, 91), left_eye)
        pygame.draw.ellipse(self.headSurf, (240, 153, 91), right_eye)

        # Pupils

        draw_rotated_ellipse(self.headSurf, (0, 0, 0),
                             pygame.Rect(cx - 75 - 16, cy - 10 - 9, 32, 18), math.degrees(m.pi / 24))
        draw_rotated_ellipse(self.headSurf, (0, 0, 0),
                             pygame.Rect(cx + 75 - 16, cy - 10 - 9, 32, 18), math.degrees(-m.pi / 24))

        # Chin
        chin_rect = pygame.Rect(cx - 46, cy + 80 - 24, 92, 48)
        pygame.draw.arc(self.headSurf, (0, 0, 0), chin_rect, m.pi / 8 + m.pi, 2 * m.pi - m.pi / 8, 7)

        # Mouth
        mouth_y = cy + 40
        bezier_curve(self.headSurf, (0, 0, 0),
                     (cx - 90, mouth_y),
                     (cx - 45, mouth_y + 20),
                     (cx - 35, mouth_y - 25),
                     (cx - 10, mouth_y - 15), 5)
        bezier_curve(self.headSurf, (0, 0, 0),
                     (cx - 10, mouth_y - 15),
                     (cx - 5, mouth_y - 13),
                     (cx + 5, mouth_y - 13),
                     (cx + 10, mouth_y - 15), 5)

        bezier_curve(self.headSurf, (0, 0, 0),
                     (cx + 10, mouth_y - 15),
                     (cx + 35, mouth_y - 25),
                     (cx + 45, mouth_y + 20),
                     (cx + 90, mouth_y), 5)

        # Nostrils

        draw_rotated_ellipse(self.headSurf, (0, 0, 0),
                             pygame.Rect(cx - 9 - 1, cy + 5 - 2, 6, 10), math.degrees(-m.pi / 6))
        draw_rotated_ellipse(self.headSurf, (0, 0, 0),
                             pygame.Rect(cx + 9 - 1, cy + 5 - 2, 6, 10), math.degrees(m.pi / 6))

    def update(self, mx, my, click):
        self.blob.update(mx, my, click)

        # Get blob points for attachment
        leftFront = self.blob.points[12].pos
        rightFront = self.blob.points[4].pos
        leftBack = self.blob.points[11].pos if len(self.blob.points) > 11 else self.blob.points[10].pos
        rightBack = self.blob.points[5].pos

        # Calculate front leg anchors with better positioning
        leftFrontAnchor = Vector(lerp(leftFront.x, rightFront.x, 0.2), lerp(leftFront.y, rightFront.y, 0.2))
        rightFrontAnchor = Vector(lerp(leftFront.x, rightFront.x, 0.8), lerp(leftFront.y, rightFront.y, 0.8))

        # Calculate body orientation for proper leg alignment
        body_center = (leftFront + rightFront + leftBack + rightBack) * 0.25
        body_direction = (rightFront - leftFront)
        if body_direction.length() > 0:
            body_direction = body_direction.normalize()
            body_normal = Vector(-body_direction.y, body_direction.x)  # Perpendicular to body direction
            body_angle = heading(body_normal)
        else:
            # Fallback if body direction is zero
            body_angle = 0

        # Calculate hind leg anchors
        leftHindAnchor = Vector(lerp(leftBack.x, rightBack.x, 0.2), lerp(leftBack.y, rightBack.y, 0.2))
        rightHindAnchor = Vector(lerp(leftBack.x, rightBack.x, 0.8), lerp(leftBack.y, rightBack.y, 0.8))

        # Update step cycle for walking animation
        self.step_cycle += self.step_speed

        # Resolve front legs with proper body orientation (passing angle, not vector)
        self.leftFrontLeg.resolve(leftFrontAnchor, body_angle)
        self.rightFrontLeg.resolve(rightFrontAnchor, body_angle)

        # Improved hind leg ground detection and movement
        left_foot_ground_dist = self.ground_level - self.leftHindLeg.foot.pos.y
        right_foot_ground_dist = self.ground_level - self.rightHindLeg.foot.pos.y

        # Ground contact logic with stepping behavior
        if left_foot_ground_dist < 20:
            self.left_hind_grounded = True
            # Apply slight ground resistance
            if left_foot_ground_dist < 0:
                self.leftHindLeg.foot.pos.y = self.ground_level
        else:
            self.left_hind_grounded = False

        if right_foot_ground_dist < 20:
            self.right_hind_grounded = True
            # Apply slight ground resistance
            if right_foot_ground_dist < 0:
                self.rightHindLeg.foot.pos.y = self.ground_level
        else:
            self.right_hind_grounded = False

        # Alternating step pattern for more natural movement
        step_offset_left = math.sin(self.step_cycle) * 15
        step_offset_right = math.sin(self.step_cycle + m.pi) * 15

        # Apply stepping motion when not grounded
        if not self.left_hind_grounded:
            target_x = leftHindAnchor.x + step_offset_left
            self.leftHindLeg.foot.pos.x = lerp(self.leftHindLeg.foot.pos.x, target_x, 0.1)

        if not self.right_hind_grounded:
            target_x = rightHindAnchor.x + step_offset_right
            self.rightHindLeg.foot.pos.x = lerp(self.rightHindLeg.foot.pos.x, target_x, 0.1)

        # Resolve hind legs with improved constraints (passing angle, not vector)
        self.leftHindLeg.resolve(leftHindAnchor, body_angle)
        self.rightHindLeg.resolve(rightHindAnchor, body_angle)

    def draw(self, surf):
        self.blob.draw(surf, (85, 145, 127), True)
        self.draw_head(surf)
        self.draw_front_legs(surf)
        self.draw_hind_legs(surf)

    def draw_head(self, surf):
        top = self.blob.points[0].pos
        # Calculate head rotation - note the angle flip for pygame
        topNormal = heading(self.blob.points[2].pos - self.blob.points[len(self.blob.points) - 2].pos)
        rotImage = pygame.transform.rotate(self.headSurf, -math.degrees(topNormal))  # Negative for pygame

        # Center the head properly with the new larger size
        head_center_x = top.x - rotImage.get_width() // 2
        head_center_y = top.y - rotImage.get_height() // 2
        surf.blit(rotImage, (head_center_x, head_center_y))

    def draw_front_legs(self, surf):
        left = self.blob.points[12].pos
        right = self.blob.points[4].pos
        leftAnchor = Vector(lerp(left.x, right.x, 0.2), lerp(left.y, right.y, 0.2))
        rightAnchor = Vector(lerp(left.x, right.x, 0.8), lerp(left.y, right.y, 0.8))
        draw_front_leg(surf, leftAnchor, self.leftFrontLeg)
        draw_front_leg(surf, rightAnchor, self.rightFrontLeg)

    def draw_hind_legs(self, surf):
        """Draw the hind legs with proper visualization"""
        left = self.blob.points[11].pos if len(self.blob.points) > 11 else self.blob.points[10].pos
        right = self.blob.points[5].pos
        leftAnchor = Vector(lerp(left.x, right.x, 0.2), lerp(left.y, right.y, 0.2))
        rightAnchor = Vector(lerp(left.x, right.x, 0.8), lerp(left.y, right.y, 0.8))

        # Draw hind legs similar to front legs
        draw_front_leg(surf, leftAnchor, self.leftHindLeg)
        draw_front_leg(surf, rightAnchor, self.rightHindLeg)