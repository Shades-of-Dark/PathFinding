import pygame
import math as m


def signed_angle(v1, v2):
    # Calculate the unsigned angle
    angle = v1.angle_to(v2)

    # Calculate the cross product to determine the sign
    cross = v1.x * v2.y - v1.y * v2.x
    if cross < 0:
        angle = -angle
    return angle


class Vector(pygame.math.Vector2):
    def normalize_angle(self, angle):
        # Bring angle within the range [0, 360)
        return angle % 360


def lerp(a, b, t):
    return a + (b - a) * t

def draw_rotated_ellipse(surf: pygame.Surface, color: (int, int, int), rect: pygame.Rect, angle: float,
                         width=0):  # angle must be in degrees
    targetrect = pygame.Rect(0, 0, rect.width, rect.height)
    shape_surf = pygame.Surface(targetrect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, targetrect, width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surf.blit(rotated_surf, rect.topleft)


def parametric_equation_circle(radius, angle, offset):
    return (radius * m.cos(angle) + offset[0], radius * m.sin(angle) + offset[1])


def cubic_bezier(t, p0, p1, p2, p3):
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return (int(x), int(y))


def relativeAngleDiff(a: float, b: float):
    result = abs(a - b)
    if result > m.pi:
        result = 2 * m.pi - result
    return result
