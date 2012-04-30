import pygame
from pygame import Rect, draw, Surface
from pygame.sprite import *
from core.settings import *

class Pickup(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.hasBounced = False

    def touches(self, group):
        touching = Group()
        coll = self.rect
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching

    def update(self, dT, level):        
        self.vY -= dT * GRAVITY_SPEED
        dX = self.vX * dT
        dY = -self.vY * dT

        # update position
        prev_rect = self.rect
        self.rect = self.rect.move(dX, dY)
        if self.rect.x < 0 or self.rect.x > level.bounds.right:
            self.direction*=-1
        self.rect.clamp_ip(level.bounds)
        
        for sprite in self.touches(level.solidTiles):
            rect = sprite.rect 
            
            # collide with walls
            if (rect.top < self.rect.bottom-2):
                if self.rect.left <= rect.right and prev_rect.left >= rect.right:
                    self.rect.left = rect.right+1
                    self.direction *=-1
                    self.vX *= -.5
                    
                if self.rect.right >= rect.left and prev_rect.right <= rect.left:
                    self.rect.right = rect.left-1
                    self.direction *=-1
                    self.vX *= -.5

            # handle landing
            if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top:
                if not ((self.rect.left <= rect.right and prev_rect.left >= rect.right) or (self.rect.right >= rect.left and prev_rect.right <= rect.left)):
                    if not self.hasBounced:
                        self.vY *= -.75
                        self.vX *= .75
                        self.hasBounced = True
                    else:
                        self.vY = 0
                        self.rect.bottom = rect.top
                        self.vX = 0

