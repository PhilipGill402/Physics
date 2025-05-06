import pygame
from Constants import *
from Ball import *

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding")
running = True
bouncyBall = Ball(100,100,10)

while running:
    surface.fill(BLACK)
    pygame.draw.rect(surface, WHITE, pygame.Rect(0, HEIGHT-50, WIDTH, 50))
    gravity = bouncyBall.mass * -9.8
    bouncyBall.addForce(0,gravity)
    bouncyBall.update(surface, WHITE)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()