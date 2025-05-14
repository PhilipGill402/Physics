from __future__ import annotations
import numpy as np
import math
from Object import *
import pygame

class AABB(Object):
    def __init__(self, x:int, y:int, width:int, height: int, velocity:np.array, mass:float, restitution:float, color:tuple):
        super().__init__(x, y, velocity, mass, restitution, color)
        self.width = width
        self.height = height
        self.max = np.array([x + (width / 2), y + (height / 2)])
        self.min = np.array([x - (width / 2), y - (height / 2)])

    def collidesWithAABB(self, object:AABB):
        if (self.max[0] < object.min[0] or self.min[0] > object.max[0]):
            return False
        if (self.max[1] < object.min[1] or self.min[1] > object.max[1]):
            return False
        return True
    
    def draw(self, surface):
        width = self.max[0] - self.min[0]
        height = self.max[1] - self.min[1]
        x = (self.min[0] + self.max[0]) / 2
        y = (self.min[1] + self.max[1]) / 2

        pygame.draw.rect(surface, self.color, pygame.Rect(x, y, width, height))
    
    def resolveCollision(self, object:Object):
        #finding the normal vector
        dx = object.x - self.x
        dy = object.y - self.y
        magnitude = math.sqrt((dx * dx) + (dy * dy))
        normal = np.array([dx / magnitude, dy / magnitude])

        #finding values needed to calculate the impulse
        relativeVelocity = self.velocity -  object.velocity
        e = min(self.restitution, object.restitution)
        velocityAlongNormal = np.dot(relativeVelocity, normal)

        #checks if objects are separating
        #if so, then no collision resolution is needed 
        if velocityAlongNormal > 0:
            return None 

        #calculating impulse scalar
        j = -1 * (1 + e) * relativeVelocity * velocityAlongNormal
        j /= (self.invMass) + (object.invMass)

        #impulse
        impulse = j * normal
        self.velocity -= (1 / self.mass) * impulse
        object.velocity += (1 / object.mass) * impulse
