import pygame
from pygame import Surface,Rect,draw
from pygame.sprite import *

class Door(Sprite):
    size = 32,32
    def __init__(self, nextLevel, loc):
        Sprite.__init__(self)
        self.rect = Rect(loc, self.size)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, (255,0,255), self.image.get_rect())
        self.nextLevel = nextLevel
        
    def draw(self, surface):
        surface.blit(self.image, (self.rect.topleft))