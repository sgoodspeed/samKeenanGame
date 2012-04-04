import pygame
from pygame.locals import *

class Player(Sprite):
    width = 20
    height = 40
    speed = 1
    def __init__(self):
        Sprite.__init__(self)
        self.startPos = (539,20)
        self.rect = Rect(self.startPos,self.width,self.height)
        self.image = Surface(self.rect.size)
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))#probably don't want this later

        #Figuring out draw needs to happen not here, dude
        pygame.draw.ellipse(self.image, (0,0,255), self.image.get_rect())
    def moveLeft(self):
        direc = (-speed,0)
        self.move(direc)
    def moveRight(self):
        direc = (speed,0)
        self.move(direc)
    
    def move(self, direction):
        self.rect.x+=direction[0]
        self.rect.y+=direction[1]

    def jump(self):
        
