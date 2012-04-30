#! /usr/bin/env python

import pygame
from pygame.locals import *

# This is used for score and lives.
class UpdateText(object):
    def __init__(self, static_text, var, loc, size = 60, color = (255,255,255)):
        self.var = var
        self.static_text = static_text
        self.color = color
        self.size = size
        self.loc = loc
    
    def draw(self, screen):
        font = pygame.font.Font(None, self.size)
        self.text = font.render(self.static_text + str(self.var), True, self.color)
        screen.blit(self.text, self.loc)
 
# This is used for the game over text, and should be used for the Pause text
class InfoText(object):
    def __init__(self, content, size = 80, color = (255, 255, 255), v_offset = 0):
        self.content = content
        self.size = size
        self.color = color
        self.v_offset = int(v_offset)

    def draw(self, screen):
        font = pygame.font.Font(None, self.size)
        self.text = font.render(self.content, True, self.color)
        
        loc = self.text.get_rect()
        loc.center = screen.get_rect().center[0], screen.get_rect().center[1] + self.v_offset
        
        screen.blit(self.text, loc)