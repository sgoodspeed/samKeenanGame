import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw

class Player(Sprite):
    width = 20
    height = 40
    size = width,height
    startPos = 100,534
    speed = 200
    vX = 0
    vY = 0
    jumping = 0
    
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
        self.vY = 550
        if self.jumping == 0:
            self.startY = self.rect.y
        self.decay = 1
        self.jumping += 1    
    
    def update(self, dT, level):
        dT /= 1000.0
        # Deal with jumping
        # If the player is currently jumping, move the player according to current Y velocity and then decrease y velocity.
        # Y velocity will continue to decrease until it's negative, thus making the player go up, slow down, and fall back down.
        if self.jumping >= 1:
            dY = int(self.vY*dT)
            self.rect.y -= dY
            self.decay += 2
            self.vY -= self.decay
        
        # Now deal with movement in the X direction
        dX = int(self.vX*dT)
        self.rect.x+=dX
