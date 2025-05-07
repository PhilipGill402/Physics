from Constants import *
import numpy as np
import pygame

class Ball:
    def __init__(self, x:float, y:float, mass:float):
        self.mass = mass
        self.position = np.array([x, y])
        self.velocity = np.array([0.0,0.0])
        self.acceleration = np.array([0.0,0.0])

    def addForce(self, forceX:int=0, forceY:int=0):
        self.acceleration[0] += (forceX/self.mass)
        self.acceleration[1] += (forceY/self.mass)

    def collidesWithBoundaries(self) -> bool:
        if self.position[1] > HEIGHT - 50 or self.position[1] < 0 or self.position[0] > WIDTH or self.position[0] < 0:
            return True
        return False
    
    def drawBall(self, surface, color:tuple):
        pygame.draw.circle(surface, color, (self.position[0], self.position[1]), self.mass)
    
    def updateVelocty(self):
        self.velocity += self.acceleration
    
    def updatePosition(self):
        self.position += self.velocity 

    def collide(self):
        if self.collidesWithBoundaries():
            self.position[1] = HEIGHT - 50 - self.mass 
            self.velocity *= -1
             
    def update(self, surface, color:tuple):
        self.updateVelocty()
        self.updatePosition()
        self.collide()
        self.drawBall(surface, color)