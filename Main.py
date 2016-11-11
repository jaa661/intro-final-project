import sys
import random
import math
import os
import getopt
import pygame
from socket import *
from pygame.locals import *
################################################################
# 
#	
#	
#	 checking things
#   
#            
#	   
 #################################################################

class Object():
        #obstacles, powerups, endgoal use inheritance
    def __init__(self):
        # --- Class Attributes ---
        # position
        self.x = 400
        self.y = 250
        self.maxspeed = 8
        self.maxacc =3
        # velocities
        self.change_x = 2
        self.change_y = -15
        # size
        self.size = 1
        # color
        self.color = [255,255,255]

    def setrect(self, x=5, y=400):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = x
        self.y = y
        
    def contains(self, Player):
        if (self.rect.colliderect(Player.rect)):
            return True
        if ((Player.x > self.x - Player.width)and(Player.x < self.x+self.width)):
            if(Player.y == self.y - Player.height ):
                return True
        if ((Player.y > self.y - Player.height)and(Player.y < self.y+self.height)):
            if(Player.x == self.x - Player.width):
                Player.walledRight = True
        if ((Player.y > self.y - Player.height)and(Player.y < self.y+self.height)):
            if(Player.x == self.x + self.width):
                Player.walledLeft = True
        #print(Player.walledLeft, Player.wwalledRight)
        return False
    def interact(self, Player):
        print("rawr")
        return 0
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.size)
#################################################################################
class endgoal(Object):
        #endgoal interact ends the game
    def __init__(self):
        # --- Class Attributes ---
        # position, top left
        self.x = 5
        self.y = 400
        self.width = 50
        self.height = 50
        # velocities//moving blocks?
        self.change_x = 0
        self.change_y = 0
        # size
        self.size = 1
        # color
        self.color = [238,136,20]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def interact(self, Player):
        return 1

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color , self.rect.move(-camera.x,0), 0 )
        pygame.draw.rect(screen, (0,0,0) , self.rect.move(-camera.x,0), self.size)

#################################################################################        
class Wall():
        #floating blocks, the ground, etc
    def __init__(self):
        # --- Class Attributes ---
        # position, top left
        self.x = 5
        self.y = 400
        self.width = 50
        self.height = 50
        # velocities//moving blocks?
        self.change_x = 0
        self.change_y = 0
        # size
        self.size = 1
        # color
        self.color = [135,134,133]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def contains(self, Player):
        if (self.rect.colliderect(Player.rect)):
            return True
        if ((Player.x > self.x - Player.width)and(Player.x < self.x+self.width)):
            if(Player.y == self.y - Player.height ):
                return True
        if ((Player.y > self.y - Player.height)and(Player.y < self.y+self.height)):
            if(Player.x == self.x - Player.width):
                Player.walledRight = True
        if ((Player.y > self.y - Player.height)and(Player.y < self.y+self.height)):
            if(Player.x == self.x + self.width):
                Player.walledLeft = True
        #print(Player.walledLeft, Player.walledRight)
        return False
    
    def setrect(self, x=5, y=400):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = x
        self.y = y
        
    def interact(self, Player):
        if(Player.x + Player.width >= self.x + self.width):
            width = self.x + self.width - Player.x
        elif(Player.x < self.x):
            width = Player.x + Player.width - self.x
        else:
            width = Player.x + Player.width

        if(Player.y + Player.height >= self.y + self.height):
            length = self.y + self.height - Player.y
        elif(Player.y < self.y):
            length = Player.y + Player.height - self.y
        else:
            length = Player.y + Player.height


        if (Player.y == self.y - Player.height):
            Player.inair = False
        elif(Player.change_y > 10):
            Player.y = self.y - Player.height
            Player.rect.y = self.y - Player.height
            Player.inair = False
            Player.change_y = 0
        elif ((Player.change_x >= 0)and(Player.change_y >= 0)):#going right, going down
            if(width>length):
                Player.y = self.y - Player.height
                Player.rect.y = self.y - Player.height
                Player.inair = False
                Player.change_y = 0
            else:
                Player.x = self.x - Player.width
                Player.rect.x = self.x - Player.width
                Player.walledRight = True
                Player.change_x = 0
        elif ((Player.change_x <= 0)and(Player.change_y >= 0)):#going left, going down
            if(width>length):
                Player.y = self.y - Player.height
                Player.rect.y = self.y - Player.height
                Player.inair = False
                Player.change_y = 0
            else:
                Player.x = self.x + self.width
                Player.rect.x = self.x + self.width
                Player.walledLeft = True
                Player.change_x = 0
        elif ((Player.change_x >= 0)and(Player.change_y <= 0)):#going right, going up
            if(length > width):
                Player.x = self.x - Player.width
                Player.rect.x = self.x - Player.width
                Player.walledRight = True
                Player.change_x = 0 
            else:
                Player.y = self.y + self.height
                Player.rect.y = self.y + self.height
                Player.change_y = 0
        elif ((Player.change_x <= 0)and(Player.change_y <= 0)):#going left, going up
            if(length > width):
                Player.x = self.x + self.width
                Player.rect.x = self.x + self.width
                Player.walledLeft = True
                Player.change_x = 0
            else:
                Player.y = self.y + self.height
                Player.rect.y = self.y + self.height
                Player.change_y = 0
        else:
            Player.inair = True

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color , self.rect.move(-camera.x,0), 0 )
        pygame.draw.rect(screen, (0,0,0) , self.rect.move(-camera.x,0), self.size)
####################################################################################

class Player():
        #this is the player
    def __init__(self):
        # --- Class Attributes ---
        # position
        self.x = 100
        self.y = 420
        self.maxspeed = 6
        self.terminal_velocity = 15
        self.maxacc =3
        self.inair = True
        self.walledRight = False
        self.walledLeft = False

        # moving?
        self.right = False
        self.left = False
        self.up = False
        # velocities
        self.change_x = 5
        self.change_y = -1

        #acceleration
        self.acc_y = 0
        self.acc_x = 0
        
        # size
        self.width = 10
        self.height = 10
        # color
        self.color = [255,255,255]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    # --- Class Methods ---
    def inAir(self):
        if self.y >= 480:
                self.inair = False
    def friction(self):
        if ((self.right == False)and(self.left == False )and(self.inair==False)):
                if (self.change_x > 0):
                        self.change_x -= 1
                if (self.change_x < 0):
                        self.change_x += 1
    def gravity(self):
        if (self.inair == True):
                self.acc_y = 1
        else:
                self.acc_y = 0
                self.change_y = 0

    def incrementX(self):
        if ((self.change_x <= 1)and(self.walledRight == False)):
            self.change_x += 2
            
    def incrementXX(self):
        self.change_x += 50
            
    def decrementX(self):
        if ((self.change_x >= -1)and(self.walledLeft == False)):
            self.change_x += -2
        
    def move_x(self):
        if ((self.right == True )and( self.change_x <= self.maxacc)and(self.walledRight == False)):
                if (self.inair == True):
                    self.acc_x += 1
                else:
                    self.acc_x += .3
                #self.walledLeft = False
        if ((self.left == True )and( self.change_x >= (-1*self.maxacc))and(self.walledLeft == False)):
                if (self.inair == True):
                    self.acc_x -= 1
                else:
                    self.acc_x -= .3
                #self.walledRight = False
        if ((self.left == False )and(self.right == False)):
                self.acc_x = 0
        if ((self.acc_x > 0) and(self.change_x <= self.maxspeed)):
                self.change_x += int(self.acc_x)
        if ((self.acc_x < 0)and( self.change_x >= (-1*self.maxspeed))):
                self.change_x += int(self.acc_x)
    

    def jump(self):
        if ((self.up == True)and(self.inair == False)):
                self.acc_y = -15
                self.up = False
                self.inair = True
        else:
                self.up = False
                                
    def update(self,camera):
        #self.inAir()
        self.gravity()
        self.jump()
        self.move_x()
        self.friction()
        #print(self.change_x, self.acc_x)
        
        if (self.change_y < self.terminal_velocity):
            self.change_y += self.acc_y
        self.x += self.change_x
        #camera.x += self.change_x
        self.y += self.change_y
        self.rect = self.rect.move(self.change_x, self.change_y)
        self.walledLeft = False
        self.walledRight = False
        #print(str(self.x) + " " + str(self.y) + " " + str(self.rect.x) + " " + str(self.rect.y))
 
    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color, self.rect.move(-camera.x, 0))
        
################################################################################
def drawMap(screen, mapstring, l, w, walls, endWalls):
    for i in range(l):
        for j in range(w):
            #print((i*w)+j)
            if(mapstring[(i*w)+j] == 'w'):
                newwall = Wall()
                newwall.setrect(50*j,50*i)
                walls.append(newwall)
            if(mapstring[(i*w)+j] == 'k'):
               schoolWall = endgoal()
               schoolWall.setrect(50*j,50*i)
               endWalls.append(schoolWall)
    
################################################################################
class Camera():
        #this is the player
    def __init__(self):
        # --- Class Attributes ---
        # position
        self.x = 0
        self.y = 0
    def update(self, Player):
        self.x = Player.x - 200
################################################################################

def main():

        mapincrease = 0
        #basic definitions
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
	# Initialise screen
        pygame.init()
        screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption('Final Project')

        # imaging
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        imageName = "background.jpg"
        backgroundimage = pygame.image.load(imageName)
        bimage = backgroundimage.convert()
        player_image = pygame.image.load("player.png").convert()
        player_image.set_colorkey(BLACK)
        background.fill((0, 0, 0))

        #background sound
        pygame.mixer.music.load('Light_It_Up.ogg')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        #pygame.mixer.music.play()#too much can be annoying

	# Display some text
        font = pygame.font.Font(None, 36)
        text = font.render("Hello world", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)

        #testmap
        walls = []
        objects = []
        onobj = False

        mapstring =  "w................................................................w.............................................................................wwwwwwwwwwwwwwwww"
        mapstring += "w...........www.......w....wwwwwwwww.......wwwwwwww..ww..........w....wwwwww....w......................w..........w..........w................wwwwwwwwwwwwwwwwww"
        mapstring += "w........ww....wwwwww..www..........wwwwww............w..........w....w.........w.................w.....wwww......w..........ww...............wwwwwwwwwwwwwwwwww"
        mapstring += "w......wwwww.................wwwww....................w..........w...ww.....wwwww................w............wwwwww.......www.w..............wwwwwwwwwwwwwwwwww"
        mapstring += "w...........wwwwwwwwwwwwwwwww.....wwwwwwwww...........wwwwww.....w.....wwww.....w...............w.................w..........w..w.............kkwwwwwwwwwwwwwwww"
        mapstring += "w..........................................wwwwwww....w......wwwwwww............w..............w.......wwwwwwww...w.....w....w...w............kkwwwwwwwwwwwwwwww"      
        mapstring += "w..................................................wwwwwwwww.................wwww.............w........www........w..........w....w...........kkwwwwwwwwwwwwwwww"   
        mapstring += "w.................................................w...wwww...wwwwwww..wwww......w............w......www..w........w..www.....w.....w.........wwwwwwwwwwwwwwwwwww"        
        mapstring += "w....wwwwww.www........................wwww......w....w..........w.........wwwwww...........w............w........w..........w......w...w...wwwwwwwwwwwwwwwwwwww"       
        mapstring += "wwwww............wwwwwwwwwwwwww..w..ww.w..ww...ww.....w..........w...wwwww......w......w...w.................................w.......w.....wwwwwwwwwwwwwwwwwwwww"        
#TEST MAP
#        mapstring =  "w.........................................................................................................................................................."
#        mapstring += "w.........................................................................................................................................................."
#        mapstring += "w.........................................................................................................................................................."
#        mapstring += "w.........................................................................................................................................................."
#        mapstring += "w.........................................................................................................................................................."
#        mapstring += "w.........................................................................................................................................................."
#        mapstring += "w.........................................................................................................................................................."
#        mapstring += "w.....................................................................................................................................kkkkkkkkkkkkkkkkkkkkk"
#        mapstring += "w.....................................................................................................................................kkkkkkkkkkkkkkkkkkkkk"
#        mapstring += "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwkkkkkkkkkkkkkkkkkkkkk"
           
        print(mapstring)
        
        drawMap(screen, mapstring, 10, 160, walls, objects)
        
	# Blit everything to the screen
        screen.blit(background, (0, 0))
        screen.blit(bimage, (0, 0))
        pygame.display.flip()

        P = Player()
        P.color = [255,0,0]

        C = Camera()
        win = 0
	# Event loop
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        while 1:
                clock.tick(30)
                for event in pygame.event.get():
                        if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                C.update(P)
                screen.blit(bimage, (0, 0))#draw background
                endTime = 120
                timeNow = (pygame.time.get_ticks() - start_time)/1000
                time = endTime - timeNow
                text = font.render(str(int(time)), 1, (255, 255, 255))
                textpos = text.get_rect()
                textpos.centerx = background.get_rect().centerx
                #draw walls in list form
                for i in range(len(walls)):
                        walls[i].draw(screen, C)
                for i in range(len(objects)):
                        objects[i].draw(screen, C)
                #draw objects in list form
                screen.blit(text, textpos)#draw timer

#                if event.type == pygame.KEYDOWN:#checks player input
#                        if (event.key == pygame.K_a and P.walledLeft == False)or(event.key == pygame.K_LEFT and P.walledLeft == False):
#                            P.left = True
#                            P.decrementX()                              
#                        if (event.key == pygame.K_d and P.walledRight == False) or(event.key == pygame.K_RIGHT and P.walledRight == False):
#                            P.right = True
#                            P.incrementX()
#                        if event.key == pygame.K_w or event.key == pygame.K_UP:
#                            P.up = True
                        #if event.key == pygame.K_q:#immediate quit
                            #break
                       # if event.key == pygame.K_e:#optional cheating
                            #P.incrementXX()
#                if event.type == pygame.KEYUP:#checks player input
#                        if event.key == pygame.K_a and event.key == pygame.K_LEFT:
#                            P.left = False
#                        if event.key == pygame.K_d and event.key == pygame.K_RIGHT:
#                            P.right = False
#                        if event.key == pygame.K_w and event.key == pygame.K_UP:
#                            P.up = False

                keys = pygame.key.get_pressed()
                if (keys[K_a] and P.walledLeft == False)or(keys[K_LEFT] and P.walledLeft == False):
                    P.left = True
                    P.decrementX()                              
                if (keys[K_d]  and P.walledRight == False) or(keys[K_RIGHT] and P.walledRight == False):
                    P.right = True
                    P.incrementX()
                if keys[K_w] or keys[K_UP]:
                    P.up = True
                if (not keys[K_a])and(not keys[K_LEFT]):
                    P.left = False
                if (not keys[K_d])and(not keys[K_RIGHT]):
                    P.right = False
                if (not keys[K_w]) and (not keys[K_UP]):
                    P.up = False
                P.update(C)#update player position based on input
                #check players position against walls and obstacles using lists
                onobj = False
                for i in range(len(walls)):
                    if walls[i].contains(P):
                        walls[i].interact(P)
                        onobj = True
                for i in range(len(objects)):
                    if objects[i].contains(P):
                        win = objects[i].interact(P)
                if onobj == False:
                    P.inair = True
                #The player reaches the end
                if(win == 1):
                    break
                if (P.y >= 500):
                    win = 0
                    break
                elif(time <= 0):
                    win = 0
                    break
                P.draw(screen, C)#draw player
                pygame.display.flip()#i think this is necessary?
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit() 
            if(win == 0):
                pygame.draw.rect(screen, (255, 255, 255), (300,200,200,100))
                text = font.render("You Lose :(", 1, (0, 0, 0))
                screen.blit(text, (310,210))

            else:
                pygame.draw.rect(screen, (255, 255, 255), (300,200,200,100))
                text = font.render("You Won!", 1, (0, 0, 0))
                screen.blit(text, (310,210))
                text = font.render("You cleared the", 1, (0, 0, 0))
                screen.blit(text, (310,230))
                text = font.render("map with:" , 1, (0, 0, 0))
                screen.blit(text, (310,250))
                text = font.render(str(int(time)) + "s left!", 1, (0, 0, 0))
                screen.blit(text, (310,270))


            P.draw(screen, C)#draw player
            pygame.display.flip()#i think this is necessary?
        #text.size(80,150)
        screen.blit(text, (225,310))
        pygame.display.flip()
        pygame.quit()
        sys.exit()
if __name__ == '__main__': main()
    


