import os

import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw
from projectiles import Bullet
from core.settings import *
from main import *

#Positions:
#1,168 CHECK
#103,232
#68,456
#248,40
#620, 552

class sampleEnemy(Sprite):
    
    def __init__(self, startPos, color):
        Sprite.__init__(self)
        self.rect = Rect(startPos,ENEMY_SIZE)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, color, self.image.get_rect())

    
    
        
