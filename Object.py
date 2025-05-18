from __future__ import annotations
import numpy as np
from Constants import *

class Object:
    def __init__(self, x:float, y:float, velocity:np.array, density:float, restitution:float, color:tuple):
        self.x = x
        self.y = y
        self.position = np.array([x, y])
        self.velocity = velocity
        self.acceleration = np.array([0.0,0.0])
        self.density = density 
        self.restitution = restitution
        self.color = color
        self.forces = []
        
    def resolveCollision(self, penetration:float, normal:np.array, object:Object):
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

        self.position = np.array([self.x, self.y])
        object.position = np.array([object.x, object.y])

    def velocityVerlet(self, dt):
        #makes sure that the object stays above the floor 
        if self.position[1] <= HEIGHT:
            self.position[0] += (self.velocity[0] * dt) + (.5 * self.acceleration[0] * dt * dt)
            self.position[1] += (self.velocity[1] * dt) + (.5 * self.acceleration[1] * dt * dt)

            self.velocity[0] += self.acceleration[0] * dt
            self.velocity[1] += self.acceleration[1] * dt
        
    def addForce(self, forceX:float, forceY:float):
        self.acceleration[0] += forceX / self.mass
        self.acceleration[1] += forceY / self.mass


        
