import pygame, sys
from pygame.locals import *


height = 80
width = 120
windowX = 800
windowY = 500
maxX = windowX-width
maxY = windowY-height
minx = 10
miny = 10

def goDirection(direction, catx):
    if direction == 'right' and catx <= maxX:
        catx += 5
    elif direction == 'left' and catx >= minx:
        catx -= 5
    else:
        catx = changeSide(direction, catx)
    return catx

def changeSide(direction, catx):
    if direction == 'right':
        catx = minx
    else:
        catx = maxX
    return catx
    
def objects():
    pygame.draw.rect(DISPLAYSURF, RED, (200, windowY-50 , 50, 50))
    return 200, windowY-50, 50, 50
    
pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()


# set up the window

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Initialise screen
pygame.init()
DISPLAYSURF = pygame.display.set_mode((windowX, windowY))
pygame.display.set_caption('Final Project')

# imaging
background = pygame.Surface(DISPLAYSURF.get_size())
background = background.convert()
imageName = "background.jpg"
backgroundimage = pygame.image.load(imageName)
bimage = backgroundimage.convert()
catImg = pygame.image.load('cat.png')
catImg.set_colorkey(BLACK)
background.fill((0, 0, 0))

RED = (255,   0,   0)
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

DISPLAYSURF.blit(bimage, (0, 0))
    
direction = 'right'
prev = 'right'

catx = minx
caty = maxY

while True: # the main game loop
    DISPLAYSURF.blit(bimage, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            prev = direction
            if event.key == pygame.K_d and catx <= maxX:
                direction = 'right'
            elif event.key == pygame.K_a and catx >= minx:
                direction = 'left'
            elif event.key == pygame.K_w and caty >= miny:
                direction = 'up'
    
    if direction == 'up':
        a = 0
        while caty >= miny and a < 20:
            DISPLAYSURF.blit(bimage, (0, 0))
            #pygame.display.flip()
            a+=1
            caty -= 5
            catx = goDirection(prev, catx)
            DISPLAYSURF.blit(catImg, (catx, caty))
            x, y, w, h = objects()
            pygame.display.update()
            fpsClock.tick(FPS)
        while caty < maxY:
            DISPLAYSURF.blit(bimage, (0, 0))
            #pygame.display.flip()
            a+=1
            caty +=5
            catx = goDirection(prev, catx)
            DISPLAYSURF.blit(catImg, (catx, caty))
            x, y, w, h = objects()
            pygame.display.update()
            fpsClock.tick(FPS)
        direction = prev
    else:
        catx = goDirection(direction, catx)
        DISPLAYSURF.blit(catImg, (catx, caty))
        x,y, w, h = objects()
        pygame.display.update()
        fpsClock.tick(FPS)
