import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw

class Player(Sprite):
    width = 20
    height = 40
    size = width,height
    startPos = 20,539
    speed = 100
    vX = 0
    vY = 0
    jumping = 0
    def __init__(self):
        Sprite.__init__(self)
        
        self.rect = Rect(self.startPos,self.size)
        self.image = Surface(self.rect.size)
        self.image.fill((0,0,0))
        
        self.image.set_colorkey((0,0,0))#probably don't want this later
        draw.rect(self.image, (0,0,255), self.image.get_rect())
        #Figuring out draw needs to happen not here, dude
        
    def move(self, direction):
        self.vX = direction * self.speed
        
    def update(self,dT):
        dT /= 1000.0
        if self.jumping>=1:
            dY = int(self.vY*dT)
            self.rect.y -=dY
            self.decay+=2
            self.vY-=self.decay
            if self.rect.y >= self.startY:
                self.jumping = 0
                self.rect.y = self.startY
                
        dX = int(self.vX*dT)
        self.rect.x+=dX
        
    def jump(self):
        self.vY = 350
        if self.jumping == 0:
            self.startY = self.rect.y
        self.decay = 1
        self.jumping += 1
