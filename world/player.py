import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw

class Player(Sprite):
    width = 20
    height = 20
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
        
    def move(self, direction):
        self.vX = direction * self.speed # This doesn't actually MOVE anything, it just sets velocity
        
    def jump(self):
        # Like move(), this doesn't actually do the jumping, it just sets up the variables and tells the player that it is now jumping. Update does the heavy lifting.
        self.vY = 350
        self.jumping +=1

    def touches(self, group):
        touching = Group()
        coll = self.rect.inflate(1,1) # grow 1px to allow for edges
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching

    def update(self, dT,level):
        dT = dT / 1000.0
        

       
        self.vY -= dT * 600
        dX = self.vX * dT
        dY = -self.vY * dT

        # update position
        prev_rect = self.rect
        self.rect = self.rect.move(dX, dY)
        self.rect.clamp_ip(level.bounds)   # temp error

        
        for sprite in self.touches(level.solidTiles):
            rect = sprite.rect 

            # collide with walls
            if self.rect.left <= rect.right and prev_rect.left >= rect.right:
                self.rect.left = rect.right
            if self.rect.right >= rect.left and prev_rect.right <= rect.left:
                self.rect.right = rect.left

            # handle cielings
            if self.rect.top <= rect.bottom and prev_rect.top >= rect.bottom:
                self.vY /= 2.0   # halve speed from hitting head
                self.rect.top = rect.bottom

            # handle landing
            if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top:
                self.vY = 0
                self.rect.bottom = rect.top-1
                self.jumping = 0
                
