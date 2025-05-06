from Constants import *
import pygame

class Ball:
    def __init__(self, x:int, y:int, mass:int):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

    def setVelocity(self, vx:int=0, vy:int=0):
        self.vx = vx
        self.vy = vy

    def addForce(self, forceX:int=0, forceY:int=0):
        self.ax += (forceX/self.mass)
        self.ay += (forceY/self.mass)
    
    def collidesWithBoundaries(self) -> bool:
        if self.y > HEIGHT - 50 or self.x > WIDTH or self.x < 0:
            return True
        return False
    
    def drawBall(self, surface, color:tuple):
        pygame.draw.circle(surface, color, (self.x, self.y), self.mass)
    
    def updateVelocty(self):
        self.vx += self.ax
        self.vy += self.ay
    
    def updatePosition(self):
        self.x += self.vx
        self.y += self.vy
    
    def update(self, surface, color:tuple):
        self.updateVelocty()
        self.updatePosition()
        self.drawBall(surface, color)