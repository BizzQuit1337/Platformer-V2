import pygame
from pygame.locals import *
import sys, random, math

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 600
WIDTH = 800
FPS = 60
FramesPerSecond = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Push-Up-Platformer")
bg = pygame.image.load("bg_01.png")

def levelFormat_floor(name, mousePos1, mousePos2):
    if mousePos1[1] != 0 and mousePos2[1] != 0:
        y = math.ceil(((mousePos1[1] + mousePos2[1])/2))
        x = math.ceil(((mousePos1[0] + mousePos2[0])/2))
        l = math.ceil(mousePos2[0] - mousePos1[0])
        print(x, y, l)
        with open(name, 'a') as f:
            f.write(str(x) + ',' + str(y) + ',' + str(l) + '\n')

def levelFormat_wall(name, mousePos1, mousePos2):
    if mousePos1[1] != 0 and mousePos2[1] != 0:
        y = math.ceil(((mousePos1[1] + mousePos2[1])/2))
        x = math.ceil(((mousePos1[0] + mousePos2[0])/2))
        l = math.ceil(mousePos2[1] - mousePos1[1])
        print(x, y, l)
        with open(name, 'a') as f:
            f.write(str(x) + ',' + str(y) + ',' + str(l) + '\n')

def coinLocation(name, mousePos1):
    if mousePos1[1] != 0:
        with open(name, 'a') as f:
            f.write(str(mousePos1[0]) + ',' + str(mousePos1[1]) + '\n')


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #print(pygame.mouse.get_pos())
                mousePos1 = pygame.mouse.get_pos()
                coinLocation('level1_coins.txt', mousePos1)
            if event.button == 3:
                mousePos2 = pygame.mouse.get_pos()
                #levelFormat_floor('level1_traps.txt', mousePos1, mousePos2)
                mousePos2 = (0, 0)

    
    
    screen.fill((0,0,0))
    screen.blit(bg, (0,0))

    pygame.display.update()
    FramesPerSecond.tick(FPS)