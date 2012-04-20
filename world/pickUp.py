import pygame
from pygame import Rect, draw, Surface
from pygame.sprite import *
from core.settings import *

class Pickup(Sprite):
    def __init__(self):
        Sprite.__init__(self)

    def touches(self, group):
        touching = Group()
        coll = self.rect
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching

    def update(self, dT, level):
        self.vX = self.direction * PICKUP_THROW_SPEED # This doesn't actually MOVE anything, it just sets velocity
        
        dT = dT / 1000.0
        
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
                    
                if self.rect.right >= rect.left and prev_rect.right <= rect.left:
                    self.rect.right = rect.left-1
                    self.direction *=-1

            # handle landing
            if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top:
                if not ((self.rect.left <= rect.right and prev_rect.left >= rect.right) or (self.rect.right >= rect.left and prev_rect.right <= rect.left)):
                    self.vY = 0
                    self.rect.bottom = rect.top
                    self.vX = 0


class AmmoPickup(Pickup):
    def __init__(self, x, y, direction, vY):
        Pickup.__init__(self)
        self.direction = direction
        self.rect = Rect((x,y), AMMO_SIZE)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, (255,0,0), self.image.get_rect())
