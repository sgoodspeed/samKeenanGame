import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import draw, Surface

# Generic Projectile Class
class Bullet(Sprite):
    size = 10
    color = 255,0,0
    speed = 400
    def __init__(self, x, y, dirX, dirY):
        Sprite.__init__(self)
        self.rect = Rect(x, y, self.size, self.size)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, self.color, self.rect)
        self.dirY = dirY
        self.dirX = dirX
    
    def update(self, dT):        
        dY = int(self.dirY*self.speed*dT)
        self.rect.y -= dY
        
        dX = int(self.dirX*self.speed*dT)
        self.rect.x+=dX