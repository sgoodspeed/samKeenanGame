import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import draw, Surface
from core.settings import *


# Generic Projectile Class
class Bullet(Sprite):
    color = 255,0,0
    def __init__(self, x, y, dirX, dirY):
        Sprite.__init__(self)
        self.rect = Rect((x, y), BULLET_SIZE)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, self.color, self.rect)
        self.dirY = dirY
        self.dirX = dirX
    
    def update(self, dT, level):        
        dY = int(self.dirY*BULLET_SPEED*dT)
        self.rect.y -= dY
        
        dX = int(self.dirX*BULLET_SPEED*dT)
        self.rect.x+=dX
        
        # Kill if we hit a solid tile
        if spritecollideany(self, level.solidTiles):
            self.kill()
        
        # Kill if we're out of the level
        if not level.bounds.contains(self.rect):
            self.kill()