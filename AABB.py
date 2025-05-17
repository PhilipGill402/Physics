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
        overlapX = min(self.max[0], object.max[0]) - max(self.min[0], object.min[0])
        overlapY = min(self.max[1], object.max[1]) - max(self.min[1], object.min[1]) 

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
        relativeVelocity = object.velocity -  self.velocity
        e = min(self.restitution, object.restitution)
        velocityAlongNormal = np.dot(relativeVelocity, normal)
        
        #checks if objects are separating
        #if so, then no collision resolution is needed 
        if velocityAlongNormal < 0:
            return None 

        #calculating impulse scalar
        j = -1 * (1 + e) * (velocityAlongNormal / ((self.invMass) + (object.invMass)))
        
        #impulse
        impulse = j * normal
        self.velocity -= self.invMass * impulse
        object.velocity += object.invMass * impulse

        #positional correction
        percent = 0.1
        slop = 0.05
        correctionMagnitude = max(penetration - slop, 0.0) / (self.invMass + object.invMass) * percent
        correction = correctionMagnitude * normal
        self.x -= correction[0] * self.invMass 
        self.y -= correction[1] * self.invMass 
        object.x += correction[0] * object.invMass 
        object.y += correction[1] * object.invMass

    def addForce(self, forceX:int, forceY:int):
        return super().addForce(forceX, forceY)

    def update(self):
        super().velocityVerlet(DT)
        self.x = self.position[0]
        self.y = self.position[1] 
        self.min = np.array([self.x, self.y])
        self.max = np.array([self.x + self.width, self.y + self.height])

        #makes small velocities 0
        if np.linalg.norm(self.velocity) < 0.01:
            self.velocity = np.array([0.0, 0.0])
 