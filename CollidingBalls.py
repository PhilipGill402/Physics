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
bouncyBall = Ball(100.0,HEIGHT-50-10.0,10.0)
bouncyBall2 = Ball(200.0,HEIGHT-50-10.0,10.0)
#ball = Ball(100.0, 150.0, 10.0)
# g = -2
gravity = bouncyBall.mass * GRAVITY 

while running:
    surface.fill(BLACK)
    pygame.draw.rect(surface, WHITE, pygame.Rect(0, HEIGHT-50, WIDTH, 50))
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                bouncyBall.velocity[0] += 10
    bouncyBall.update(surface, WHITE)
    pygame.display.update()
    time.sleep(0.025)

pygame.quit()