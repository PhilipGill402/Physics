import pygame
import time
import numpy as np
from Constants import *
from Ball import *

# REMEMBER: right is positive and left is negative
# REMEMBER: up is negative and down is positive
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncy Ball")
running = True
bouncyBall = Ball(100.0,100.0,10.0)
gravity = bouncyBall.mass * 5

while running:
    surface.fill(BLACK)
    pygame.draw.rect(surface, WHITE, pygame.Rect(0, HEIGHT-50, WIDTH, 50))
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                bouncyBall.addForce(0,gravity)
    
    bouncyBall.update(surface, WHITE)
    print(bouncyBall.acceleration)
    pygame.display.update()
    time.sleep(0.025)

pygame.quit()