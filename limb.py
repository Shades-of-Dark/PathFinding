from util import Vector, heading, constrainAngle
import math as m
from point import Point
import pygame.draw


class Limb:
    def __init__(self, origin, distance, elbowRange, elbowOffset, footRange, footOffset):
        self.distance = distance
        self.elbowRange = elbowRange
        self.elbowOffset = elbowOffset
        self.footRange = footRange
        self.footOffset = footOffset
        self.elbow = LimbPoint(Vector(origin[0], origin[1] + distance))
        self.foot = LimbPoint(Vector(origin[0], origin[1] + distance * 2))

    def resolve(self, anchor, normal):
        # Resolve elbow first
        self.elbow.verletIntegrate()
        self.elbow.applyGravity()
        self.elbow.applyConstraint(anchor, normal, self.distance, self.elbowRange, self.elbowOffset)
        self.elbow.keepInBounds()

        # Resolve foot relative to elbow
        self.foot.verletIntegrate()
        self.foot.applyGravity()
        # Use the elbow's calculated angle for the foot constraint
        elbow_to_anchor = anchor - self.elbow.pos
        elbow_angle = heading(elbow_to_anchor) if elbow_to_anchor.length() > 0 else 0
        self.foot.applyConstraint(self.elbow.pos, elbow_angle, self.distance, self.footRange, self.footOffset)
        self.foot.keepInBounds()

    def draw(self, surf, anchor):
        pygame.draw.line(surf, (0, 0, 0), anchor.xy, self.elbow.pos.xy, 8)
        pygame.draw.line(surf, (0, 0, 0), self.elbow.pos.xy, self.foot.pos.xy, 8)

        pygame.draw.ellipse(surf, (42, 44, 53), pygame.Rect(anchor.x - 16, anchor.y - 16, 32, 32))
        pygame.draw.ellipse(surf, (42, 44, 53), pygame.Rect(self.elbow.pos.x - 16, self.elbow.pos.y - 16, 32, 32))
        pygame.draw.ellipse(surf, (42, 44, 53), pygame.Rect(self.foot.pos.x - 16, self.foot.pos.y - 16, 32, 32))


class LimbPoint(Point):
    def __init__(self, pos: Vector):
        super().__init__(pos)
        self.angle = 0

    def verletIntegrate(self):
        temp = self.pos.copy()
        vel = self.pos - self.ppos
        vel *= 0.95  # dampened vel
        self.pos = temp + vel  # Actually apply the velocity!
        self.ppos = temp

    def applyConstraint(self, anchor, normal, distance, angleRange, angleOffset):
        # Calculate the target angle
        anchorAngle = normal + angleOffset

        # Get current angle from anchor to this point
        to_point = self.pos - anchor
        if to_point.length() > 0:
            curAngle = heading(to_point)
        else:
            curAngle = anchorAngle

        # Constrain the angle within the allowed range
        constrainedAngle = constrainAngle(curAngle, anchorAngle, angleRange)

        # Calculate the constrained position
        rotvec = Vector(m.cos(constrainedAngle), m.sin(constrainedAngle))
        rotvec.scale_to_length(distance)
        self.pos = anchor + rotvec  # Add, not subtract!

        # Store the angle for potential use by connected limb segments
        self.angle = constrainedAngle
