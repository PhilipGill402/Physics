import pygame
import numpy as np
from Constants import *
from AABB import *
from Ball import *
from Spring import *

# REMEMBER: right is positive and left is negative
# REMEMBER: up is negative and down is positive
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()
running = True
dragging = False

spring = Spring(100.0, 100.0, 50.0, 50.0, 100.0, 10.0, WHITE)
topBorder = AABB(0.0, 0.0, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
bottomBorder = AABB(0.0, HEIGHT, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
leftBorder = AABB(-10.0, 0.0, 10.0, HEIGHT, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
rightBorder = AABB(WIDTH, 0.0, 10.0, HEIGHT, np.array([0.0,0.0]), 0.0, 1.0, WHITE)

objectList = []
objectList.append(topBorder)
objectList.append(bottomBorder) 
objectList.append(leftBorder)
objectList.append(rightBorder)

while running:
    clock.tick(1 / DT)
    surface.fill(BLACK)
    pos = pygame.mouse.get_pos()
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.MOUSEBUTTONDOWN:

            if spring.isInside(pos):
                dx = 0
                prevX = pos[0]
                dragging = True
        if ev.type == pygame.MOUSEBUTTONUP:
            dragging = False
            spring.amplitude = spring.ballX - spring.eq
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                spring.update()

    for i in range(len(objectList)):
        for j in range(i + 1, len(objectList)):
            A = objectList[i]
            B = objectList[j]
            if type(A) == AABB and type(B) == AABB:
                if A.collidesWithAABB(B):
                    A.resolveAABBCollision(B)
            elif type(A) == AABB and type(B) == Ball:
                if A.collidesWithBall(B):
                    A.resolveBallCollision(B)
            elif type(A) == Ball and type(B) == Ball:
                if A.collidesWithBall(B):
                    A.resolveBallCollision(B)
            elif type(A) == Ball and type(B) == AABB:
                if A.collidesWithAABB(B):
                    A.resolveAABBCollision(B)

        objectList[i].addForce(np.array([0.0,9.8*objectList[i].mass])) 
        objectList[i].draw(surface)
        objectList[i].update()
    
    if dragging:
        if pos[0] > spring.x + spring.width + (spring.width / 4):
            spring.ballX = pos[0]
            spring.springWidth = spring.ballX - spring.x - spring.width
    else:
        spring.update()
    spring.draw(surface)
    

    
    pygame.display.update()

pygame.quit()