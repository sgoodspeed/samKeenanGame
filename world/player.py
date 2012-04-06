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
        self.vY = 350
        if self.jumping == 0:
            self.startY = self.rect.y
        self.decay = 1
        self.jumping += 1    
    
    def update(self, dT, level):
        # Stop if it hits a solid tile
        onGround = False
        for rect in level.solids:
            if self.rect.colliderect(rect) and rect.top > self.rect.top and self.jumping > 0:
                self.rect.bottom = rect.top-1
                self.vY = 0
                self.jumping = 0
                onGround = True
                print "onground true"
            if self.rect.colliderect(rect) and rect.bottom < self.rect.bottom and self.jumping > 0:
                self.vY -= self.vY*2
            if self.rect.colliderect(rect) and rect.left > self.rect.left:
                self.rect.left -= 5
                self.vX = 0
            if self.rect.colliderect(rect) and rect.right > self.rect.right:
                self.rect.right += self.width
                self.vX = 0
                
        if not onGround and self.jumping <= 0:
            self.vY = -10
            """
            this is some code that doesn't work
            # Can't jump through ceilings
            if rect.collidepoint(self.rect.topleft) and rect.collidepoint(self.rect.bottomleft):
                self.vX = 0;
                print "left"
            elif rect.collidepoint(self.rect.topright) and rect.collidepoint(self.rect.bottomright):
                self.vX = 0
                print "right"
            elif rect.collidepoint(self.rect.topleft) and rect.collidepoint(self.rect.topright):
                    self.rect.top = rect.bottom
                    self.vY -= self.vY*2
                    print "top"
            # Stop falling if we hit the floor and end the jump routine
            elif rect.collidepoint(self.rect.bottomleft) and rect.collidepoint(self.rect.bottomright):
                    print "bottom"
                    #if self.jumping > 0 and self.vY < 0:
                    self.rect.bottom = rect.top
                    self.vY = 0
                    self.jumping = 0"""
    
        dT /= 1000.0
        # Deal with jumping
        # If the player is currently jumping, move the player according to current Y velocity and then decrease y velocity.
        # Y velocity will continue to decrease until it's negative, thus making the player go up, slow down, and fall back down.
        if self.jumping>=1:
            dY = int(self.vY*dT)
            self.rect.y -= dY
            self.decay += 2
            self.vY -= self.decay
        
        # Now deal with movement in the X direction
        dX = int(self.vX*dT)
        self.rect.x+=dX
