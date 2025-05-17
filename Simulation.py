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
clock = pygame.time.Clock()
running = True

square = AABB(100.0, HEIGHT - 50, 50, 50, np.array([0.0,0.0]), 10, 1.0, WHITE)
anotherSquare = AABB(500.0, HEIGHT - 50, 50, 50, np.array([0.0,0.0]), 10, 1.0, WHITE)

topBorder = AABB(0.0, 0.0, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
bottomBorder = AABB(0.0, HEIGHT, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
leftBorder = AABB(0.0, 0.0, 10.0, HEIGHT, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
rightBorder = AABB(WIDTH-10.0, 0.0, 10.0, HEIGHT, np.array([0.0,0.0]), 0.0, 1.0, WHITE)

objectList = []
objectList.append(topBorder)
objectList.append(bottomBorder) 
objectList.append(leftBorder)
objectList.append(rightBorder)
objectList.append(square)
objectList.append(anotherSquare)

while running:
    clock.tick(1 / DT)
    surface.fill(BLACK)
    x, y = pygame.mouse.get_pos()
    #print(x,y) 
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                square.velocity[0] = 50 
                anotherSquare.velocity[0] = -50

    for i in objectList:
        for j in objectList:
            if (not i == j) and type(i) == AABB and type(j) == AABB:
                if i.collidesWithAABB(j):
                    i.resolveAABBCollision(j)

        i.draw(surface)
        i.update()
    
    pygame.display.update()

pygame.quit()