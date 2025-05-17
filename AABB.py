from __future__ import annotations
import numpy as np
import math
from Object import *
from Ball import Ball
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
    
    def collidesWithBall(self, object:Ball):
        closest = np.maximum(self.min, np.minimum(object.position, self.max))
        difference = object.position - closest
        
        if np.dot(difference, difference) < object.radius ** 2:
            return True
        return False

    def resolveAABBCollision(self, object: AABB):
        if not self.collidesWithAABB(object):
            return None

        #checks case if both masses are immovable
        if self.invMass + object.invMass == 0:
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

        super().resolveCollision(penetration, normal, object)

    def resolveBallCollision(self, object:Ball):
        #checks if both objects are immovable
        if self.invMass + object.invMass == 0:
            return None

        #manifold generation
        closest = np.maximum(self.min, np.minimum(object.position, self.max))
        print(closest)
        difference = self.position - closest
        differenceSquared = np.dot(difference, difference)
        distance = np.sqrt(differenceSquared)

        if distance != 0:
            normal = difference / distance
            print(difference)
            print(distance)
            print(normal)
            penetration = max(object.radius - distance, 0.0)
        else:
            center = (self.max + self.min) / 2
            dx = object.position[0] - center[0]
            dy = object.position[1] - center[1]

            if abs(dx) > abs(dy):
                if dx > 0:
                    normal = np.array([1.0,0.0])
                else:
                    normal = np.array([-1.0,0.0])
                penetration = object.radius + (self.max[0] - self.min[0]) / 2 - abs(dx)

            else:
                if dy > 0:
                    normal = np.array([0.0,1.0])
                else:
                    normal = np.array([0.0,-1.0])
                penetration = object.radius + (self.max[1] - self.min[1]) / 2 - abs(dy)

        super().resolveCollision(penetration, normal, object)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], self.width, self.height))

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
 