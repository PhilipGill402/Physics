import pygame
import time
import numpy as np
from Constants import *
from AABB import *

# REMEMBER: right is positive and left is negative
# REMEMBER: up is negative and down is positive
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")
running = True

square = AABB(100.0, HEIGHT - 50, 50, 50, np.array([0.0,0.0]), 10, 0.5, WHITE)
anotherSquare = AABB(500.0, HEIGHT - 50, 50, 50, np.array([0.0,0.0]), 10, 0.5, WHITE)

topBorder = AABB(0.0, 0.0, WIDTH, 1.0, np.array([0,0]), 0.0, 1.0, WHITE)
bottomBorder = AABB(0.0, HEIGHT, WIDTH, 1.0, np.array([0,0]), 0.0, 1.0, WHITE)
leftBorder = AABB(0.0, 0.0, 1.0, HEIGHT, np.array([0,0]), 0.0, 1.0, WHITE)
rightBorder = AABB(WIDTH, 0.0, 1.0, HEIGHT, np.array([0,0]), 0.0, 1.0, WHITE)

while running:
    surface.fill(BLACK)
    x, y = pygame.mouse.get_pos()
    #print(x,y) 
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                square.acceleration[0] = 10
                anotherSquare.acceleration[0] = -10
    
    square.draw(surface)
    anotherSquare.draw(surface)
    square.update()
    anotherSquare.update() 
    if square.collidesWithAABB(anotherSquare):
        square.resolveAABBCollision(anotherSquare)
       #print(square.velocity)
       #print(anotherSquare.velocity) 
    pygame.display.update()
pygame.quit()