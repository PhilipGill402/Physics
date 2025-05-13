from Constants import *
import numpy as np
import pygame

class Ball:
    def __init__(self, x:float, y:float, mass:float, bounciness:float=0):
        self.mass = mass
        self.position = np.array([x, y])
        self.velocity = np.array([0.0,0.0])
        self.acceleration = np.array([0.0,0.0])
        self.bounciness = bounciness

    def addForce(self, forceX:int=0, forceY:int=0):
        self.acceleration[0] += (forceX/self.mass)
        self.acceleration[1] += (forceY/self.mass)

    def collidesWithLeftBoundary(self) -> bool:
        if self.position[0] < 0:
            return True
        return False

    def collidesWithRightBoundary(self) -> bool:
        if self.position[0] > WIDTH:
            return True
        return False

    def collidesWithFloor(self) -> bool:
        if self.position[1] > HEIGHT - 50:
            return True
        return False
    
    def collidesWithRoof(self) -> bool:
        if self.position[1] < 0:
            return True
        return False
    
    def drawBall(self, surface, color:tuple):
        pygame.draw.circle(surface, color, (self.position[0], self.position[1]), self.mass)
    
    def updateVelocity(self):
        self.velocity += self.acceleration
    
    def updatePosition(self):
        self.position += self.velocity 

    def collide(self):
        if self.collidesWithFloor():
            self.addForce(0, -1 * self.mass * GRAVITY) #normal force 

        if self.collidesWithRoof():
            self.position[1] = 0
            self.velocity *= -1 
        
        if self.collidesWithLeftBoundary():
            self.position[0] = 0
            self.velocity *= -1
        
        if self.collidesWithRightBoundary():
            self.position[0] = WIDTH
            self.velocity *= -1
             
    def update(self, surface, color:tuple):
        self.updateVelocity()
        self.updatePosition()
        self.collide()
        self.drawBall(surface, color)
        self.addForce(0, self.mass * GRAVITY)