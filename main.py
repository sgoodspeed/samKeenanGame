#!/usr/bin/env python

import os
import pygame
from pygame.locals import *

from core.settings import *
from core.input import InputManager, KeyListener, MouseListener
from core.app import Application
from core.hud import *
from world.player import *
from world.enemies import *
from core.level import *
from pygame.sprite import *
from core.cameraJunk.camera import *
from world.door import Door
from core.collisions import collisionCheck

#Continuing on with melee attacks: the draw isn't working, it's because the function for melee attack runs once each time you press it, rather than continuously ten times through when the key is pressed once. Ideas: While loop, sepratare method, etc.


# controls/player.py
# This is a combination mouse and key listener which we then pass to input manager
class PlayerController(KeyListener, MouseListener):
    k_moveLeft = K_LEFT
    k_moveRight = K_RIGHT
    def __init__(self, player):
        self.player = player
        self.pressed = {}
        

    def on_keydown(self, event):
        self.pressed[event.key] = True
        if not self.player.thrown:
            if event.key == K_SPACE and self.player.jumping < PLAYER_MAX_JUMPS:
               self.player.jump() 
        
            elif event.key == K_z:
                self.player.shoot()
            elif event.key == K_x:
                self.player.meleeAttack()
            
            
    def update(self):
        if self.pressed.get(self.k_moveLeft) and self.pressed.get(self.k_moveRight):
            self.player.move(0)
        elif self.pressed.get(self.k_moveLeft):
            self.player.move(-1)
        elif self.pressed.get(self.k_moveRight):
            self.player.move(1)
        else:
            self.player.move(0)
        
            
    def on_keyup(self,event):
        self.pressed[event.key] = False
        if event.key == K_LEFT or event.key == K_RIGHT:
            self.player.vX = 0


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
        self.pc = PlayerController(self.player)
        self.input.add_key_listener(self.pc)

        #Create Hud instance
        self.gameHud = Hud(self.player.health,self.hud)

        
                
        
                
        # Create the sound effects controller and give it a keyboard listener as well
        sc = SfxController(self.sounds, self)
        self.input.add_key_listener(sc)
        
        # Load the tilemap image, build a tilesheet out of it and render the tilesheet into an image which we can blit to the screen
        self.levels = []
        self.img_tiles = load_image(TILEMAP_IMAGE, (0,255,200))
        self.tileSheet = TileSheet(self.img_tiles, (TILE_SIZE)) 
        
        # Create an array of all the levels
        for levelFile in LEVELS:
            self.levels.append(Level(levelFile, self.tileSheet))
            
        for key,link in enumerate(LEVEL_LINKS):
            door = Door(self.levels[link], (150,504))
            self.levels[key].addDoor(door)
    
        self.currLevel = self.levels[0]
        self.count = 0

        #Camera init
        self.cam = Camera(self.player,self.currLevel.bounds,self.gameArea.get_size())

    def changeLevel(self, nextLevel):
        self.currLevel = nextLevel
        self.player.changeLevel()

    def update(self):
        # update
        dT = min(200, self.clock.get_time())
        self.pc.update()
        collisionCheck(self.playerGroup, self.currLevel.enemies, self.currLevel.ammo, self.currLevel)
        
        self.cam.update(self.player.rect)
        
        self.playerGroup.update(dT, self.currLevel)
        self.currLevel.enemies.update(dT, self.currLevel) # We shouldn't need to pass self.currLevel to a group that's owned by currLevel
        
        if self.currLevel.door.rect.colliderect(self.player.rect):
            self.changeLevel(self.currLevel.door.nextLevel)

        self.currLevel.ammo.update(dT, self.currLevel)
        
        #player collision with sample enemy
        #for self.player in pygame.sprite.groupcollide(self.playerGroup,self.sampleEnemyGroup,False,True):
         #   self.player.health-=15
    
    def draw(self, screen):
        # draw
        
        self.cam.draw_background(self.gameArea, self.currLevel.background)
        self.cam.draw_sprite(self.gameArea, self.player)
        self.cam.draw_sprite_group(self.gameArea, self.player.bullets)
        self.cam.draw_sprite_group(self.gameArea,self.player.meleeGroup)
        self.cam.draw_sprite_group(self.gameArea, self.currLevel.enemies)
        self.cam.draw_sprite_group(self.gameArea, self.currLevel.ammo)
        pygame.display.flip() # Refresh the screen
        
        self.gameHud.hudDraw(self.player.health)


if __name__ == "__main__":
    game = Game()
    game.run()

pygame.quit()
print "Program complete"
