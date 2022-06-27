import pygame
from pygame.locals import *
import sys, random, math, time

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 600
WIDTH = 800
ACC = 0.5
FRIC = -0.2
FPS = 60
FramesPerSecond = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Push-Up-Platformer")
bg = pygame.image.load("bg_01.png")
mousePos1 = (0, 0)
mousePos2 = (0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.surf = pygame.Surface((30, 45))
        self.surf = pygame.image.load('eric_right.png')
        #self.surf.fill((70, 92, 105))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.score = 0

    def move(self):
        self.acc = vec(0,0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load('eric_left.png')
            self.rect = self.surf.get_rect()
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load('eric_right.png')
            self.rect = self.surf.get_rect()
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
    
    def jump(self):
        hitFloor = pygame.sprite.spritecollide(self, all_floors, False)
        if hitFloor:
           self.vel.y = -15
    
    def scoreFun(counter):
        number = pygame.image.load('N' + str(counter) + '.png')
        screen.blit(number, (0,0))

    
    def update(self):
        hitFloor = pygame.sprite.spritecollide(self, all_floors, False)
        hitWall = pygame.sprite.spritecollide(self, all_walls, False)
        hitCeiling = pygame.sprite.spritecollide(self, all_ceilings, False)
        hitFlag = pygame.sprite.spritecollide(self, all_flags, False)
        hitTrap = pygame.sprite.spritecollide(self, all_traps, False)
        hitCoin = pygame.sprite.spritecollide(self, all_coins, True)
        if hitFlag:
            if self.score == 5:
                print('you win!!!!')
            else:
                print('you need at least 5 coins')
        if hitTrap:
            self.pos.x = 250
            self.pos.y = 250
            self.score = 0
        if hitCoin:
            self.score = self.score + 1
        if self.vel.y > 0:
            if hitFloor:
                self.vel.y = 0
                self.pos.y = hitFloor[0].rect.top + 1
        if self.vel.y < 0:
            if hitCeiling:
                self.vel.y = -self.vel.y
                self.vel.x = -self.vel.x
                self.pos.y = hitCeiling[0].rect.bottom + 25
        if self.vel.x > 0:
            if hitWall:
                self.pos.x = hitWall[0].rect.left - 16
                self.vel.x = -self.vel.x
        elif self.vel.x < 0:
            if hitWall:
                self.pos.x = hitWall[0].rect.right + 16
                self.vel.x = -self.vel.x
        number = pygame.image.load('N' + str(self.score) + '.png')
        screen.blit(number, (0,0))
        

class Floor(pygame.sprite.Sprite):
    def __init__(self, posX, posY, length):
        super().__init__()
        self.surf = pygame.Surface((length, 3))
        self.surf.fill((115, 82, 144))
        self.rect = self.surf.get_rect(center = (posX, posY))

    def move(self):
        pass

class Wall(pygame.sprite.Sprite):
    def __init__(self, posX, posY, height):
        super().__init__()
        self.surf = pygame.Surface((3, height))
        self.surf.fill((115, 82, 144))
        self.rect = self.surf.get_rect(center = (posX, posY))

    def move(self):
        pass

class Ceiling(pygame.sprite.Sprite):
    def __init__(self, posX, posY, length):
        super().__init__()
        self.surf = pygame.Surface((length, 3))
        self.surf.fill((115, 82, 144))
        self.rect = self.surf.get_rect(center = (posX, posY))

    def move(self):
        pass

class Flag(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 200, 0))
        self.rect = self.surf.get_rect(center = (posX, posY))
    def move(self):
        pass

class Traps(pygame.sprite.Sprite):
    def __init__(self, posX, posY, length):
        super().__init__()
        self.surf = pygame.Surface((length, 20))
        self.surf.fill((200, 13, 46))
        self.rect = self.surf.get_rect(center = (posX, posY))

    def move(self):
        pass

class Coin(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        #self.surf = pygame.Surface((20, 20))
        self.surf = pygame.image.load('coin.png')
        #self.surf.fill((255, 0, 255))
        self.rect = self.surf.get_rect(center = (posX, posY))

    def move(self):
        pass

def floorLevel1(file, type):
    floorLevel1.all = []
    floorCount = 0
    with open(file, 'r') as f:
        for line in f:
            sl = line.split(',')
            name = 'F' + str(floorCount)
            name = type(int(sl[0]), int(sl[1]), int(sl[2][:3]))
            floorLevel1.all.append(name)
            floorCount = floorCount + 1

def wallLevel1(file):
    wallLevel1.all = []
    wallCount = 0
    with open(file, 'r') as f:
        for line in f:
            sl = line.split(',')
            name = 'F' + str(wallCount)
            name = Wall(int(sl[0]), int(sl[1]), int(sl[2][:3]))
            wallLevel1.all.append(name)
            wallCount = wallCount + 1

def coinsLevel1(file):
    coinsLevel1.all = []
    coinCount = 0
    with open(file, 'r') as f:
        for line in f:
            sc = line.split(',')
            name = 'C' + str(coinCount)
            name = Coin(int(sc[0]), int(sc[1][:3]))
            coinsLevel1.all.append(name)



P1 = Player()
Fl1 = Flag(758, 74)

floorLevel1('level1_floor.txt', Floor) 
floors = floorLevel1.all  

floorLevel1('level1_ceil.txt', Ceiling)  
ceils = floorLevel1.all 

wallLevel1('level1_walls.txt')
walls = wallLevel1.all

floorLevel1('level1_traps.txt', Traps)
traps = floorLevel1.all

coinsLevel1('level1_coins.txt')
coins = coinsLevel1.all

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(Fl1)
all_sprites.add(floors)
all_sprites.add(ceils)
all_sprites.add(walls)
all_sprites.add(traps)
all_sprites.add(coins)

all_floors = pygame.sprite.Group()
all_floors.add(floors)

all_walls = pygame.sprite.Group()
all_walls.add(walls)

all_ceilings = pygame.sprite.Group()
all_ceilings.add(ceils)

all_flags = pygame.sprite.Group()
all_flags.add(Fl1)

all_traps = pygame.sprite.Group()
all_traps.add(traps)

all_coins = pygame.sprite.Group()
all_coins.add(coins)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_UP:
                P1.jump()
    
    screen.fill((0,0,0))
    screen.blit(bg, (0,0))
    P1.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramesPerSecond.tick(FPS)