import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw
from projectiles import Bullet
from core.settings import *

class Player(Sprite):
    vX = 0
    vY = 0
    jumping = 0
    decay = 0
    gravity = True
    
    def __init__(self):
        Sprite.__init__(self)

        self.rect = Rect(PLAYER_START, PLAYER_SIZE) # Build the player's rect
        self.image = Surface(self.rect.size) # Give the player a surface the size of the rect
        self.image.fill((0,0,0)) # Fill the surface with black
        
        self.image.set_colorkey((0,0,0)) # Probably don't want this later
        draw.rect(self.image, (0,0,255), self.image.get_rect()) # This draws the visible blue rectangle (We only draw this image once. Then, the spritegroup that Player is a part of moves the player's Surface (which has the image we just drew) around)
        
        self.direction = 1
        
        self.bullets = Group()

        self.health = 100
        
    def move(self, direction):
        self.vX = direction * PLAYER_SPEED # This doesn't actually MOVE anything, it just sets velocity
        self.direction = direction
        
    def jump(self):
        # Like move(), this doesn't actually do the jumping, it just sets up the variables and tells the player that it is now jumping. Update does the heavy lifting.
        self.vY = PLAYER_JUMP_SPEED
        self.jumping +=1

    def changeLevel(self):
        self.rect.x = PLAYER_START_X
        self.rect.y = PLAYER_START_Y
        self.vY = 0
        self.vX = 0
        self.jumping = 0
        self.bullets.empty()

    def touches(self, group):
        touching = Group()
        coll = self.rect
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching

    def update(self, dT, level):
        dT = dT / 1000.0
        
        self.vY -= dT * GRAVITY_SPEED
        dX = self.vX * dT
        dY = -self.vY * dT

        self.bullets.update(dT, level)            

        # update position
        prev_rect = self.rect
        self.rect = self.rect.move(dX, dY)
        self.rect.clamp_ip(level.bounds)   # temp error
        
        for sprite in self.touches(level.solidTiles):
            rect = sprite.rect 
            
            # collide with walls
            if (self.jumping == 0 and rect.top < self.rect.bottom-2) or (self.jumping > 0 and rect.top < self.rect.bottom):
                if self.rect.left <= rect.right and prev_rect.left >= rect.right:
                    self.rect.left = rect.right
                if self.rect.right >= rect.left and prev_rect.right <= rect.left:
                    self.rect.right = rect.left


            # handle cielings
            if rect.left < self.rect.right and self.rect.left < rect.right:
                if self.rect.top <= rect.bottom and prev_rect.top >= rect.bottom:
                    self.vY /= 2.0   # halve speed from hitting head
                    self.rect.top = rect.bottom

            # handle landing
            if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top:
                if self.jumping == 0 and not ((self.rect.left <= rect.right and prev_rect.left >= rect.right) or (self.rect.right >= rect.left and prev_rect.right <= rect.left)):
                    self.vY = 0
                    self.rect.bottom = rect.top
                    self.jumping = 0
                elif self.jumping > 0 and not ((self.rect.left <= rect.right and prev_rect.left >= rect.right) or (self.rect.right >= rect.left and prev_rect.right <= rect.left)):
                    self.jumping = 0
                    self.rect.bottom = rect.top
                    
                    

                    
    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y, self.direction, 0)
        self.bullets.add(bullet)
    
    def takeDamage(self,damageAmount):
        self.health-=damageAmount
        if self.health <=0:
            print "slefslefslefslefslefslef"     
