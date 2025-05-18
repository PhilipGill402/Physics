import pygame
import numpy as np
import random
from Constants import *
from AABB import *
from Ball import *

# REMEMBER: right is positive and left is negative
# REMEMBER: up is negative and down is positive
def generateVelocity() -> np.array:
    vx = random.randint(-50,50)
    vy = random.randint(-50,50)
    velocity = np.array([vx, vy])
    normal = np.linalg.norm(velocity)
    if normal == 0:
        return velocity
    else:
        return velocity / normal    

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 28)
running = True
leftPaddle = AABB(30.0, HEIGHT / 2 - 50.0, 15.0, 100.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
rightPaddle = AABB(WIDTH - 30.0, HEIGHT / 2 - 50.0, 15.0, 100.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
ball = Ball(WIDTH / 2, HEIGHT / 2, 10, np.array([0.0,0.0]), 10.0, 1.0, WHITE)

topBorder = AABB(0.0, 0.0, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
bottomBorder = AABB(0.0, HEIGHT, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)

objectList = []
objectList.append(topBorder)
objectList.append(bottomBorder) 
objectList.append(ball)
objectList.append(leftPaddle)
objectList.append(rightPaddle)
leftScore = 0
rightScore = 0

while running:
    clock.tick(1 / DT)
    surface.fill(BLACK)
    score = font.render(f"P1: {leftScore} | P2: {rightScore}", True, WHITE)
    scoreRect = score.get_rect()
    scoreRect.center = (WIDTH / 2, 25) 
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                ball.velocity = generateVelocity() * 400 

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and rightPaddle.position[1] < HEIGHT - 100:
        rightPaddle.position[1] += 5
    elif keys[pygame.K_UP] and rightPaddle.position[1] > 0:
        rightPaddle.position[1] -= 5
    elif keys[pygame.K_w] and leftPaddle.position[1] > 0:
        leftPaddle.position[1] -= 5
    elif keys[pygame.K_s] and leftPaddle.position[1] < HEIGHT - 100:
        leftPaddle.position[1] += 5

    if ball.collidesWithAABB(leftPaddle):
        ball.resolveAABBCollision(leftPaddle) 
    elif ball.collidesWithAABB(rightPaddle):
        ball.resolveAABBCollision(rightPaddle)
    elif ball.collidesWithAABB(topBorder):
        ball.resolveAABBCollision(topBorder)
    elif ball.collidesWithAABB(bottomBorder):
        ball.resolveAABBCollision(bottomBorder)
    elif ball.position[0] > WIDTH:
        leftScore += 1
        ball.position = np.array([WIDTH / 2, HEIGHT / 2])
        ball.velocity = generateVelocity() * 400
    elif ball.position[0] < 0:
        rightScore += 1
        ball.position = np.array([WIDTH / 2, HEIGHT / 2])     
        ball.velocity = generateVelocity() * 400

    surface.blit(score, scoreRect)
    for i in objectList:
        i.update()
        i.draw(surface)
    pygame.display.update()

pygame.quit()