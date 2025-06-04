import pygame
import numpy as np
import random
from Constants import *
from AABB import *
from Ball import *
from Spring import *

# REMEMBER: right is positive and left is negative
# REMEMBER: up is negative and down is positive
def drawPegs(surface, objectList:list):
    y = 50
    amount = 3
    spacing = 50
    center = WIDTH / 2
    while y != HEIGHT - 100: 
        if amount % 2 != 0:
            peg = Ball(center, y, 10.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
            objectList.append(peg)
            for i in range(1, amount):
                peg = Ball(center + (((-1) ** i) * spacing * math.ceil(i / 2)), y, 10.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
                objectList.append(peg)
        else:
            for i in range(1, amount + 1):
                peg = Ball(center + (((-1) ** i) * (25 + 50 * ((i - 1) // 2))), y, 10.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
                objectList.append(peg)
        amount += 1
        y += 50
    
    return amount

def drawBins(surface, numBins:int, objectList:list):
    multipliers = [120, 14, 5.2, 1.4, 0.4, 0.2, 0.2, 0.4, 1.4, 5.2, 14, 120]
    for i in range(numBins):
        bin = AABB((i * 50) + 162.5, HEIGHT - 100, 35.0, 10.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
        objectList.append(bin)
        mult = font.render(str(multipliers[i]), True, BLACK)
        multRect = mult.get_rect()
        multRect.center = ((i * 50) + 162.5, HEIGHT - 100)
        surface.blit(mult, multRect)

def drawMultipliers(surface, multipliers):
    for i in range(len(multipliers)):
        mult = font.render(str(multipliers[i]), True, BLACK)
        multRect = mult.get_rect()
        multRect.center = ((i * 50) + 180, HEIGHT - 95)
        surface.blit(mult, multRect)

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko")
clock = pygame.time.Clock()
running = True
falling = False
font = pygame.font.Font('freesansbold.ttf', 10)
bigFont = pygame.font.Font('freesansbold.ttf', 24)
money = 100
multipliers = [43, 7, 2, 0.6, 0.2, 0.2, 0.6, 2, 7, 43]
gameBall = None

restitution = random.uniform(0.15, 0.25)

topBorder = AABB(0.0, 0.0, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
bottomBorder = AABB(0.0, HEIGHT, WIDTH, 1.0, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
leftBorder = AABB(-10.0, 0.0, 10.0, HEIGHT, np.array([0.0,0.0]), 0.0, 1.0, WHITE)
rightBorder = AABB(WIDTH, 0.0, 10.0, HEIGHT, np.array([0.0,0.0]), 0.0, 1.0, WHITE)

objectList = []

amount = drawPegs(surface, objectList)
drawBins(surface, amount - 2, objectList)
objectList.append(topBorder)
objectList.append(bottomBorder) 
objectList.append(leftBorder)
objectList.append(rightBorder)

while running:
    clock.tick(1 / DT)
    surface.fill(BLACK)
    pos = pygame.mouse.get_pos()
    moneyText = bigFont.render(f"${money}", True, WHITE)
    moneyTextRect = moneyText.get_rect()
    moneyTextRect.center = (50,50)
    surface.blit(moneyText, moneyTextRect)    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pass
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE and not falling:
                x = random.randint((WIDTH // 2) - 50, (WIDTH // 2) + 50)
                gameBall = Ball(x, 20.0, 8.0, np.array([0.0,0.0]), 10.0, restitution, WHITE)
                objectList.append(gameBall)
                falling = True 
                money -= 10

    collides = False 
    for i in range(len(objectList)):
        for j in range(i + 1, len(objectList)):
            A = objectList[i]
            B = objectList[j]
            if type(A) == AABB and type(B) == AABB:
                if A.collidesWithAABB(B):
                    A.resolveAABBCollision(B)
            elif type(A) == AABB and type(B) == Ball:
                if A.collidesWithBall(B):
                    collides = True
            elif type(A) == Ball and type(B) == Ball:
                if A.collidesWithBall(B):
                    A.resolveBallCollision(B)
            elif type(A) == Ball and type(B) == AABB:
                if A.collidesWithAABB(B):
                    A.resolveAABBCollision(B)

        
        if type(objectList[i]) != Ball:
            objectList[i].addForce(np.array([0.0,9.8*objectList[i].mass]))
        elif objectList[i] == gameBall and falling:
            objectList[i].addForce(np.array([0.0,100*objectList[i].mass]))
        objectList[i].draw(surface)
        objectList[i].update()

    if collides:
        idx = math.floor((gameBall.position[0] - 162.5) / 50)
        money += 10 * multipliers[idx]
        objectList.pop(-1)
        collides = False
        falling = False

    drawMultipliers(surface, multipliers) 
    pygame.display.update()

pygame.quit()