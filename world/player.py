import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect

class Player(Sprite):
    width = 20
    height = 40
    speed = 1
    def __init__(self):
        Sprite.__init__(self)
        self.startPos = (539,20)
        self.rect = Rect(10,10,self.width,self.height)
        self.image = Surface(self.rect.size)
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))#probably don't want this later
        
        #Figuring out draw needs to happen not here, dude
        
    
    
    def move(self, direction):
        print "We are moving"
        self.rect.x+=direction*self.speed
        

    
    def draw(self):
        print "We are drawing"
        pygame.draw.ellipse(self.image, (0,0,255), self.image.get_rect())
    
    def jump(self):
        pass
