from pygame import Surface,Rect,draw
from pygame.sprite import *
from core.settings import *


class Door(Sprite):
    def __init__(self, nextLevel, loc):
        Sprite.__init__(self)
        self.rect = Rect(loc, TILE_SIZE)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, (255,0,255), self.image.get_rect()) ## REPLACE THIS WITH AN IMAGE
        self.nextLevel = nextLevel
        
    def draw(self, surface):
        surface.blit(self.image, (self.rect.topleft))
