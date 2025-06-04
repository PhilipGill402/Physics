from __future__ import annotations
from Constants import *
from Object import *
from AABB import *
import numpy as np
import pygame
import math

class Ball(Object):
    def __init__(self, x:float, y:float, radius:float, velocity:np.array, density:float, restitution:float, color:tuple):
        super().__init__(x, y, velocity, density, restitution, color)
        self.radius = radius
        self.mass = .5 * math.pi * radius ** 2 * density
        if self.mass == 0:
            self.invMass = 0
        else:
            self.invMass = 1 / self.mass

    def __distance(self, object:Object):
        dx = self.x - object.x 
        dy = self.y - object.y 
        distance = math.sqrt(dx**2 + dy**2)
        return distance 

    def collidesWithBall(self, object:Ball):
        distance = self.__distance(object)
        if distance < (self.radius + object.radius):
            return True
        return False

    def collidesWithAABB(self, object:AABB):
        closest = np.maximum(object.min, np.minimum(self.position, object.max))
        difference = self.position - closest
        
        if np.dot(difference, difference) < self.radius ** 2:
            return True
        return False
    
    def resolveBallCollision(self, object:Ball):
        if self.invMass + object.invMass == 0:
            return None

        n = self.position - object.position
        distance = self.__distance(object)
        radiusSum = self.radius + object.radius

        if distance == 0:
            normal = np.array([1.0,0.0])
            penetration = self.radius
        else:
            normal = n / distance
            penetration = radiusSum - distance

        super().resolveCollision(penetration, normal, object)

        
    
    def resolveAABBCollision(self, object:AABB):
        #checks if both objects are immovable
        if self.invMass + object.invMass == 0:
            return None

        #manifold generation
        closest = np.maximum(object.min, np.minimum(self.position, object.max))
        difference = self.position - closest
        differenceSquared = np.dot(difference, difference)
        distance = np.sqrt(differenceSquared)
        
        if distance != 0:
            normal = difference / distance
            penetration = self.radius - distance
        else:
            center = (object.max + object.min) / 2
            dx = self.position[0] - center[0]
            dy = self.position[1] - center[1]

            if abs(dx) > abs(dy):
                if dx > 0: 
                    normal = np.array([1.0,0.0])
                else:
                    normal = np.array([-1.0,0.0])
                penetration = self.radius + (object.max[0] - object.min[0]) / 2 - abs(dx)

            else:
                if dy > 0:
                    normal = np.array([0.0,1.0])
                else:
                    normal = np.array([0.0,-1.0])
                penetration = self.radius + (object.max[1] - object.min[1]) / 2 - abs(dy)

        super().resolveCollision(penetration, normal, object) 
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.position[0], self.position[1]), self.radius)

    def update(self):
        super().velocityVerlet(DT)
        self.x = self.position[0]
        self.y = self.position[1]
        self.acceleration = self.forces * self.invMass
        self.forces = np.array([0.0,0.0])

        #makes small velocities 0
        if np.linalg.norm(self.velocity) < 0.01:
            self.velocity = np.array([0.0, 0.0])