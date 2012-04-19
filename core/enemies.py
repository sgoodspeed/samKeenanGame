import os

import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw
from world.projectiles import Bullet
from core.settings import *
from main import *
from random import *
class rat(Sprite):
    vY = 0
    vX = 0
    damage = RAT_DAMAGE
    health = RAT_HEALTH
    def __init__(self, startPos):
        Sprite.__init__(self)
        self.direction = randrange(-1,2,2)
        self.rect = Rect(startPos,RAT_SIZE)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, (143,55,0), self.image.get_rect())

    def touches(self, group):
        touching = Group()
        coll = self.rect
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching

    def update(self, dT, level):
        self.vX = self.direction * RAT_SPEED # This doesn't actually MOVE anything, it just sets velocity
        
        dT = dT / 1000.0
        
        self.vY -= dT * GRAVITY_SPEED
        dX = self.vX * dT
        dY = -self.vY * dT

        
        
        # update position
        prev_rect = self.rect
        self.rect = self.rect.move(dX, dY)
        if self.rect.x < 0 or self.rect.x > level.bounds.right:
            self.direction*=-1
        self.rect.clamp_ip(level.bounds)   # temp error
        
        for sprite in self.touches(level.solidTiles):
            rect = sprite.rect 
            
            # collide with walls
            if (rect.top < self.rect.bottom-2):
                if self.rect.left <= rect.right and prev_rect.left >= rect.right:
                    self.rect.left = rect.right
                    self.direction *=-1
                if self.rect.right >= rect.left and prev_rect.right <= rect.left:
                    self.rect.right = rect.left
                    self.direction *=-1

            # handle cielings
            #if rect.left < self.rect.right and self.rect.left < rect.right:
             #   if self.rect.top <= rect.bottom and prev_rect.top >= rect.bottom:
              #      self.vY /= 2.0   # halve speed from hitting head
               #     self.rect.top = rect.bottom

            # handle landing
            if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top:
                if not ((self.rect.left <= rect.right and prev_rect.left >= rect.right) or (self.rect.right >= rect.left and prev_rect.right <= rect.left)):
                    self.vY = 0
                    self.rect.bottom = rect.top
                    #self.jumping = 0
                
    def takeDamage(self, damageAmount):
        self.health-=damageAmount
        if self.health <=0:
            self.kill()