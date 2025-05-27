import pygame
import math
from Constants import *

class Spring():
    def __init__(self, x:float, y:float, width:float, height:float, k:float, mass:float, color:tuple):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.k = k
        self.mass = mass
        self.color = color
        self.springHeight = self.height / 8
        self.eq = self.x + 3*self.width #can't change
        self.amplitude = 0 
        self.ballX = self.x + 3*self.width
        self.ballY = self.y + self.height / 2 
        self.springWidth = self.ballX - self.x - self.width
        self.velocity = 0
        self.time = 0

    def isInside(self, pos:tuple) -> bool:
        currX, currY = pos
        dx = currX - self.ballX 
        dy = currY - self.ballY 
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance <= self.width / 4 

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x + self.width, self.y + (7/16) * self.height, self.springWidth, self.springHeight))
        pygame.draw.circle(surface, self.color, (self.ballX, self.ballY), self.width / 4)
    
    def update(self) -> None:
        if self.ballX <= self.x + self.width + (self.width / 4):
            self.ballX = self.x + self.width + self.width / 4
            self.velocity *= -1
        dx = self.ballX - self.eq
        acceleration = - (self.k * dx) / self.mass   
        self.ballX += (self.velocity * DT) + (.5 * acceleration * DT * DT)
        
        newDX = self.ballX - self.eq
        newAcceleration = - (self.k * newDX) / self.mass
        self.velocity += .5 * (acceleration + newAcceleration) * DT 
        self.springWidth = self.ballX - self.x - self.width