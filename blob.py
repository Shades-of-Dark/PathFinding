import pygame.draw
from point import Point
from util import Vector, catmull_rom_point, generate_spline_points
from math import *

WIDTH, HEIGHT = 1920, 1080


class Blob():
    def __init__(self, origin: Vector, numPoints: int, radius: float, puffiness: float):
        self.radius = radius
        self.area = radius * radius * pi * puffiness
        self.circumference = radius * 2 * pi
        self.chordLength = self.circumference / numPoints
        self.points = []
        for i in range(numPoints):
            offset: Vector = Vector(cos(2 * pi * i / numPoints - pi / 2) * radius,
                                    sin(2 * pi * i / numPoints - pi / 2) * radius)
            self.points.append(BlobPoint(origin + offset))

    def getArea(self):
        sum1 = 0
        sum2 = 0
        for i in range(len(self.points)):
            cur = self.points[i].pos
            nextP = self.points[0 if i == len(self.points) - 1 else i + 1].pos
            sum1 += (cur.x * nextP.y)
            sum2 += (cur.y * nextP.x)

        return abs(sum2 - sum1) / 2

    def update(self, mx, my, click):
        for point in self.points:
            point.verletIntegrate()
            point.applyGravity()

        # Very tight distance constraints for firm jello consistency
        for _ in range(10):  # More iterations for very tight control
            for i in range(len(self.points)):
                cur = self.points[i]
                nextP = self.points[(i + 1) % len(self.points)]
                diff = nextP.pos - cur.pos
                distance = diff.length()

                if distance > 0:
                    # Very tight bounds - minimal deformation allowed
                    min_dist = self.chordLength * 0.95  # Allow only 5% compression
                    max_dist = self.chordLength * 1.08  # Allow only 8% stretching

                    target_distance = self.chordLength
                    if distance < min_dist:
                        target_distance = min_dist
                    elif distance > max_dist:
                        target_distance = max_dist

                    error = distance - target_distance
                    correction_strength = 0.9  # Very strong correction
                    offset = diff.normalize() * error * correction_strength
                    cur.accumulateDisplacement(offset * 0.9)
                    nextP.accumulateDisplacement(-offset * 0.9)

        # Very strong area constraint for firm shape
        current_area = self.getArea()
        area_error = self.area - current_area
        area_ratio = current_area / self.area if self.area > 0 else 1

        # Aggressive area correction - very tight tolerance
        if area_ratio < 0.9 or area_ratio > 1.12:  # Very tight area tolerance
            amount = area_error / self.circumference * 0.4  # Strong correction

            # Calculate center of mass
            center = Vector(0, 0)
            for p in self.points:
                center += p.pos
            center /= len(self.points)

            # Strong radial correction to maintain perfect circular shape
            for i, point in enumerate(self.points):
                to_center = point.pos - center
                current_radius = to_center.length()

                if current_radius > 0:
                    # Strong area correction
                    area_correction = to_center.normalize() * amount

                    # Strong radius normalization for perfect circle
                    target_radius = self.radius
                    radius_error = target_radius - current_radius
                    radius_correction = to_center.normalize() * radius_error  # Stronger

                    total_correction = area_correction + radius_correction
                    point.accumulateDisplacement(total_correction)

        for point in self.points:
            point.applyDisplacement()
            point.keepInBounds()
            point.collideWithMouse(mx, my, click)

    def draw(self, surf, color, outline):
        # Generate smooth spline points
        spline_points = generate_spline_points(self.points, resolution=15)

        # Convert Vector objects to tuples for pygame
        point_tuples = [(int(p.x), int(p.y)) for p in spline_points]

        # Draw the smooth blob using the spline points
        if len(point_tuples) >= 3:
            pygame.draw.polygon(surf, color, point_tuples)
            if outline:
                pygame.draw.lines(surf, (0, 0, 0), False, point_tuples + [point_tuples[0]], 8)
        # Optional: Draw the control points for debugging
        # for point in self.points:
        #     pygame.draw.circle(surf, (255, 0, 0), (int(point.pos.x), int(point.pos.y)), 3)


class BlobPoint(Point):
    def __init__(self, pos: Vector):
        super().__init__(pos)
        self.displacement = Vector(0, 0)
        self.displacementWeight = 0

    def verletIntegrate(self):
        temp = self.pos.copy()
        vel = self.pos - self.ppos

        # Increased damping for more stable behavior
        vel *= 0.99  # More damping

        self.pos += vel
        self.ppos = temp

    def accumulateDisplacement(self, offset: Vector):
        self.displacement += offset
        self.displacementWeight += 1

    def applyDisplacement(self):
        if self.displacementWeight > 0:
            # Average the displacements and apply with moderate strength
            self.displacement /= self.displacementWeight
            self.pos += self.displacement * 0.8  # Apply 80% of correction for stability
            self.displacement = Vector(0, 0)
            self.displacementWeight = 0

    def collideWithMouse(self, mx, my, mousePressed):
        mouse = Vector(mx, my)
        if mousePressed and dist(self.pos.xy, mouse.xy) < 100:
            diff = self.pos - mouse
            if diff.length() != 0:
                diff.scale_to_length(100)
                self.pos = mouse + diff
