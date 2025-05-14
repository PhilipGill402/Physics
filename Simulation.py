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

square = AABB(100, 100, 50, 50, np.array([0.0,0.0]), 10, 0.5, WHITE)
anotherSquare = AABB(200, 200, 50, 50, np.array([0.0,0.0]), 10, 0.5, WHITE)

while running:
    surface.fill(BLACK)
    pygame.draw.rect(surface, WHITE, pygame.Rect(0, HEIGHT-50, WIDTH, 50))
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                pass
    square.draw(surface)
    anotherSquare.draw(surface)
    if square.collidesWithAABB(anotherSquare):
        square.resolveCollision(anotherSquare) 
    pygame.display.update()
    time.sleep(0.025)

pygame.quit()