from pygame import Surface,Rect,draw
from pygame.sprite import *
from core.settings import *


class Door(Sprite):
    def __init__(self, nextLevel, loc,image,openImage):
        Sprite.__init__(self)
        self.openImage = openImage
       
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = loc
        self.nextLevel = nextLevel
        
    def draw(self, surface):
        surface.blit(self.image, (self.rect.topleft))
    
    def open(self):
        self.image = self.openImage
