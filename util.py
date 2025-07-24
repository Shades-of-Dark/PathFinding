import pygame
import math as m


def catmull_rom_point(p0, p1, p2, p3, t):
    """Calculate a point on a Catmull-Rom spline"""
    t2 = t * t
    t3 = t2 * t

    # Catmull-Rom basis functions
    b0 = -0.5 * t3 + t2 - 0.5 * t
    b1 = 1.5 * t3 - 2.5 * t2 + 1
    b2 = -1.5 * t3 + 2 * t2 + 0.5 * t
    b3 = 0.5 * t3 - 0.5 * t2

    x = b0 * p0.x + b1 * p1.x + b2 * p2.x + b3 * p3.x
    y = b0 * p0.y + b1 * p1.y + b2 * p2.y + b3 * p3.y

    return Vector(x, y)


def generate_spline_points(points, resolution=20):
    """Generate smooth curve points using Catmull-Rom splines"""
    if len(points) < 3:
        return [p.pos for p in points]

    spline_points = []
    num_points = len(points)

    for i in range(num_points):
        # Get the four control points for this segment
        p0 = points[(i - 1) % num_points].pos
        p1 = points[i].pos
        p2 = points[(i + 1) % num_points].pos
        p3 = points[(i + 2) % num_points].pos

        # Generate points along the curve segment
        for j in range(resolution):
            t = j / resolution
            point = catmull_rom_point(p0, p1, p2, p3, t)
            spline_points.append(point)

    return spline_points


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


def constrain(a, minim, maxim):
    return max(min(maxim, a), minim)


def heading(v: Vector):
    angle = m.atan2(v.y, v.x)
    if angle > 0:
        angle -= m.pi * 2
    return angle


def simplifyAngle(angle):
    while angle >= 2 * m.pi:
        angle -= 2 * m.pi  # just gets you a coterminal angle
    while angle < 0:
        angle += 2 * m.pi
    return angle


def normalizeAngle(angle):
    """Normalize angle to (-π, π] range"""
    while angle > m.pi:
        angle -= 2 * m.pi
    while angle <= -m.pi:
        angle += 2 * m.pi
    return angle


def signedAngleDiff(a: float, b: float):
    """Returns the signed difference between two angles (a - b), accounting for wrapping"""
    diff = a - b
    if diff > m.pi:
        diff -= 2 * m.pi
    elif diff < -m.pi:
        diff += 2 * m.pi
    return diff


def constrainAngle(angle, anchor, constraint):
    """
    Constrain an angle to be within ±constraint of the anchor angle.

    Args:
        angle: The angle to constrain
        anchor: The center/reference angle
        constraint: The maximum allowed deviation from anchor (in radians)

    Returns:
        The constrained angle
    """
    # Normalize both angles to the same range for consistent comparison
    angle = normalizeAngle(angle)
    anchor = normalizeAngle(anchor)

    # Calculate the signed difference
    diff = signedAngleDiff(angle, anchor)

    # If within constraint, return original angle
    if abs(diff) <= constraint:
        return simplifyAngle(angle)

    # Constrain to the appropriate boundary
    if diff > constraint:
        # angle is too far in positive direction
        constrained = anchor + constraint
    else:
        # angle is too far in negative direction
        constrained = anchor - constraint

    return simplifyAngle(constrained)
