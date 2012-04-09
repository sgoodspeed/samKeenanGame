#!/usr/bin/env python

import os
import pygame
from pygame.locals import *

from core.input import InputManager, KeyListener, MouseListener
from core.app import Application
from world.player import *
from tiles import *
from pygame.sprite import *
from core.cameraJunk.camera import *


# controls/player.py
# This is a combination mouse and key listener which we then pass to input manager
class PlayerController(KeyListener, MouseListener):
    def __init__(self, player):
        self.player = player

    def on_keydown(self, event):
        if event.key == K_SPACE and self.player.jumping < 2:
            self.player.jump() #Note to future selves: You guys look handsome and you should figure out key repeat exemptions for jumping so that holding space doesn't double jump
        if event.key == K_LEFT:
            self.player.move(-1)
        if event.key == K_RIGHT:
            self.player.move(1)
        if event.key == K_z:
            self.player.shoot()

    def on_keyup(self,event):
        if event.key == K_LEFT or event.key == K_RIGHT:
            self.player.vX = 0

# This is just testing stuff
class LevelController(KeyListener):
    def __init__(self, level, tilesheet, levelNum):
        self.level = level
        self.tilesheet = tilesheet
        self.levelNum = levelNum
        
    def on_keydown(self, event):
        if event.key == K_e:
            self.nextLevel()
        if event.key == K_w:
            self.prevLevel()
            
    def nextLevel(self):
        self.levelNum += 1
        self.level.__init__("level"+str(self.levelNum), self.tilesheet)
    
    def prevLevel(self):
        self.levelNum -= 1
        self.level.__init__("level"+str(self.levelNum), self.tilesheet)

# controls/sound.py
class SfxController(KeyListener):
    def __init__(self, sm, game):
        self.game = game
        self.sm = sm

    def on_keydown(self, event):
        pass



class Game(Application):
    def __init__(self):
        Application.__init__(self)
        
        # Create player and put it in a spritegroup
        self.player = Player()
        self.playerGroup = pygame.sprite.GroupSingle(self.player)
        
        # Create the PlayerController and pass it player and add a keyboard listener to it
        pc = PlayerController(self.player)
        self.input.add_key_listener(pc)
                
        # Create the sound effects controller and give it a keyboard listener as well
        sc = SfxController(self.sounds, self)
        self.input.add_key_listener(sc)
        
        # Load the tilemap image, build a tilesheet out of it and render the tilesheet into an image which we can blit to the screen
        self.levelNum = 1;
        self.img_tiles = load_image("tiles", (0,255,200))
        self.tilesheet = TileSheet(self.img_tiles, (32, 32))
        self.level = Level("level"+str(self.levelNum), self.tilesheet)
        
        
        self.lc = LevelController(self.level, self.tilesheet, self.levelNum)
        self.input.add_key_listener(self.lc)
        
        # Create the group of solids
        

        #Camera init
        self.cam = Camera(self.player,self.level.bounds,self.gameArea.get_size())

    def update(self):
        # update
        dT = self.clock.get_time()
        
        self.cam.update(self.player.rect)
        self.playerGroup.update(dT, self.level, self.lc)            
    
    def draw(self, screen):
        # draw

        self.cam.draw_background(self.gameArea, self.level.background)
        self.cam.draw_sprite(self.gameArea, self.player)
        self.cam.draw_sprite_group(self.gameArea, self.player.bullets)
        pygame.display.flip() # Refresh the screen


if __name__ == "__main__":
    game = Game()
    game.run()

pygame.quit()
print "Program complete"
