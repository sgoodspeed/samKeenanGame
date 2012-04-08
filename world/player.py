import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw
from projectiles import Bullet

class Player(Sprite):
    width = 20
    height = 40
    size = width,height
    startPos = 100,504
    speed = 200
    vX = 0
    vY = 0
    jumping = 0
    decay = 0
    gravity = True
    
    def __init__(self):
        Sprite.__init__(self)

        self.rect = Rect(self.startPos,self.size) # Build the player's rect
        self.image = Surface(self.rect.size) # Give the player a surface the size of the rect
        self.image.fill((0,0,0)) # Fill the surface with black
        
        self.image.set_colorkey((0,0,0)) # Probably don't want this later
        draw.rect(self.image, (0,0,255), self.image.get_rect()) # This draws the visible blue rectangle (We only draw this image once. Then, the spritegroup that Player is a part of moves the player's Surface (which has the image we just drew) around)
        
        self.direction = 1
        
        self.bullets = Group()
        
    def move(self, direction):
        self.vX = direction * self.speed # This doesn't actually MOVE anything, it just sets velocity
        self.direction = direction
        
    def jump(self):
        # Like move(), this doesn't actually do the jumping, it just sets up the variables and tells the player that it is now jumping. Update does the heavy lifting.
        self.vY = 350
        self.decay = 1
        self.jumping += 1
        self.gravity = True    
    
    def update(self, dT, level):                    
        dT /= 1000.0
        # Deal with jumping
        # If the player is currently jumping, move the player according to current Y velocity and then decrease y velocity.
        # Y velocity will continue to decrease until it's negative, thus making the player go up, slow down, and fall back down.
        if self.gravity:
            self.vY -= self.decay
            if self.decay < 32:
                self.decay += 2
            
        
        #if self.jumping >= 1:
        dY = int(self.vY*dT)
        self.rect.y -= dY
        
        # Now deal with movement in the X direction
        dX = int(self.vX*dT)
        self.rect.x+=dX
        
        self.bullets.update(dT, level)
        
        for tile in level.solidTiles:
            if (tile.rect.collidepoint(self.rect.bottomleft) or tile.rect.collidepoint(self.rect.bottomright)) and not tile.rect.collidepoint(self.rect.topright) and not tile.rect.collidepoint(self.rect.topleft):
                self.gravity = False
                self.jumping = 0
                self.rect.bottom = tile.rect.top
            if tile.rect.collidepoint(self.rect.topleft) or tile.rect.collidepoint(self.rect.topright) and self.jumping > 0:
                self.vY = 0
                #self.rect.top = tile.rect.bottom
                self.decay += 2
            if tile.rect.collidepoint(self.rect.topleft):
                self.vX = 0
                self.rect.left += 2
            if tile.rect.collidepoint(self.rect.topright):
                self.vX = 0
                self.rect.right -= 2
                    
                    
    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y, self.direction, 0)
        self.bullets.add(bullet)
