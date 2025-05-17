import numpy as np
from Constants import *

class Object:
    def __init__(self, x:float, y:float, velocity:np.array, mass:float, restitution:float, color:tuple):
        self.x = x
        self.y = y
        self.position = np.array([x, y])
        self.velocity = velocity
        self.acceleration = np.array([0.0,0.0])
        self.mass = mass
        self.restitution = restitution
        self.color = color
        if self.mass == 0:
            self.invMass = 0
        else:
            self.invMass = 1 / self.mass

        
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


    def update(self):
       self.velocityVerlet(0.001)
        
