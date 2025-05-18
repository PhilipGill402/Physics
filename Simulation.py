import pygame
import numpy as np
from Constants import *
from AABB import *
from Ball import *

# REMEMBER: right is positive and left is negative
# REMEMBER: up is negative and down is positive
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()
running = True

square = AABB(175.0, HEIGHT - 50, 50, 50, np.array([0.0,0.0]), 10, 1.0, WHITE)
anotherSquare = AABB(375.0, HEIGHT - 50, 50, 50, np.array([0.0,0.0]), 10, 1.0, WHITE)
ball = Ball(100.0, HEIGHT - 10, 10, np.array([0.0,0.0]), 10.0, 1.0, WHITE)
anotherBall = Ball(500.0, HEIGHT - 10, 10, np.array([0.0,0.0]), 50.0, 1.0, WHITE)

topBorder = AABB(0.0, 0.0, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
bottomBorder = AABB(0.0, HEIGHT, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
leftBorder = AABB(-10.0, 0.0, 10.0, HEIGHT, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
rightBorder = AABB(WIDTH, 0.0, 10.0, HEIGHT, np.array([0.0,0.0]), 0.0, 1.0, WHITE)

objectList = []
objectList.append(topBorder)
objectList.append(bottomBorder) 
objectList.append(leftBorder)
objectList.append(rightBorder)
objectList.append(ball)
objectList.append(anotherBall)
objectList.append(square)
objectList.append(anotherSquare)


while running:
    clock.tick(1 / DT)
    surface.fill(BLACK)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                ball.velocity[0] = 50 
                anotherBall.velocity[0] = -50

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
    
        objectList[i].draw(surface)
        objectList[i].update()
    
    pygame.display.update()

pygame.quit()