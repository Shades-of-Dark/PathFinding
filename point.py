from util import Vector, constrain

WIDTH, HEIGHT = 1920, 1080

class Point:
    def __init__(self, pos: Vector):
        self.pos = pos.copy()
        self.ppos = pos.copy()

    def applyGravity(self):
        self.pos.y += 0.2

    def keepInBounds(self):
        self.pos.x = constrain(self.pos.x, 10, WIDTH - 10)
        self.pos.y = constrain(self.pos.y, 10, HEIGHT - 10)
