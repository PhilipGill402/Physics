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
        self.max = np.array([x + width, y + height])
        self.min = np.array([x, y])

    def collidesWithAABB(self, object:AABB):
        if (self.max[0] < object.min[0] or self.min[0] > object.max[0]):
            return False 
        if (self.max[1] < object.min[1] or self.min[1] > object.max[1]):
            return False 
        return True 
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], self.width, self.height))

    def resolveAABBCollision(self, object: AABB):
        if not self.collidesWithAABB(object):
            return None
        
        #Manifold Generation
        overlapX = min(self.x, object.x) - max(self.x, object.x)
        overlapY = min(self.y, object.y) - max(self.y, object.y)

        if overlapX < overlapY:
            penetration = overlapX
            if self.x + (self.width / 2) < object.x + (object.width / 2):
                normal = np.array([-1, 0])
            else:
                normal = np.array([1, 0])
        else:
            penetration = overlapY
            if self.y + (self.height / 2) < object.y + (object.height / 2):
                normal = np.array([0, -1])
            else:
                normal = np.array([0, 1])

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

        #positional correction
        percent = 0.2
        slop = 0.01
        correctionMagnitude = max(penetration - slop, 0.0) / ((1 / self.mass) + (1 / object.mass)) * percent
        correction = correctionMagnitude * normal
        self.x -= correction[0] * (1 / self.mass)
        self.y -= correction[1] * (1 / self.mass)
        object.x += correction[0] * (1 / object.mass)
        object.y += correction[1] * (1 / object.mass)

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
    
    def addForce(self, forceX:int, forceY:int):
        return super().addForce(forceX, forceY)

    def update(self):
        return super().velocityVerlet(DT) 