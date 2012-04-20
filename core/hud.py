import os
import pygame
from pygame.locals import *

from core.app import Application
from world.player import *



class Hud (object):

    def __init__(self,health,hud):
        
        self.surf = hud
        self.health = health
        self.healthBar = Rect(10,10,health*2,20)
        
        
    def hudDraw(self,curHealth):
        if self.health != curHealth:
            self.health = curHealth
            self.surf.fill((0,0,0))
            self.healthBar = Rect(10,10,self.health*2,20)
        
        if self.health>20:
            self.healthColor = (0,255,0)
        else:
            self.healthColor = (255,0,0)
        if self.health>0:
            pygame.draw.rect(self.surf,(0,0,0),self.healthBar)
            pygame.draw.rect(self.surf,self.healthColor,self.healthBar)
