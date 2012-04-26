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



# controls/player.py
# This is a combination mouse and key listener which we then pass to input manager
class PlayerController(KeyListener, MouseListener):
    k_moveLeft = K_LEFT
    k_moveRight = K_RIGHT
    def __init__(self, player):
        self.timer = 0
        self.mel = False
        self.coolDown = False
        self.player = player
        self.pressed = {}
        

    def on_keydown(self, event):
        self.pressed[event.key] = True
        if not self.player.thrown:
            if event.key == K_SPACE and self.player.jumping < PLAYER_MAX_JUMPS:
               self.player.jump() 
        
            elif event.key == K_z:
                self.player.shoot()
            elif event.key == K_x and not self.mel:
                self.player.meleeAttack()
                self.mel = True
            elif event.key == K_UP and not self.player.doorChange:
                self.player.doorChange = True
                
            
    def update(self, dT):
        self.dT = dT
        if self.mel:
            self.timer+=self.dT
            #print self.timer
        if self.timer > 1000:
            self.mel = False
            self.timer = 0

            
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
        elif event.key == K_UP and self.player.doorChange:
            self.player.doorChange = False


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

        #Level change variable(s??)
        self.changing = False

        self.timer = 0
        self.check = False
        self.fadeAlpha = 255
        
        self.fadeScreen = Surface(self.gameArea.get_size())
        self.fadeScreen.fill((0,0,0))
        self.fadeScreen.set_alpha(0)
                
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
    
    def changeLevel(self, nextLevel,dT):
        self.timer += dT
        self.gameArea.fill((0,0,0))
        if self.timer < 1500:
            self.fadeAlpha -= 10
            #self.cam.draw_sprite_alpha(self.gameArea, self.player, self.fadeAlpha+5)
            self.cam.draw_background_alpha(self.gameArea, self.currLevel.background, self.fadeAlpha)
            self.check = True
            
        if self.timer > 1500 and self.check:
            self.currLevel = nextLevel
            self.player.changeLevel()
            #self.cam.draw_background_alpha(self.gameArea, self.currLevel.background, 0)
            #self.cam.draw_sprite_alpha(self.gameArea, self.player, 0)
            self.check = False
            
        if self.timer < 3000 and self.timer > 1500:
            self.fadeAlpha += 10
            self.cam.draw_background_alpha(self.gameArea, self.currLevel.background, self.fadeAlpha)
            #self.cam.draw_sprite_alpha(self.gameArea, self.player, self.fadeAlpha)

            
        if self.timer > 3000:    
            self.timer = 0
            self.changing = False
    

    def update(self):
        # update
        dT = min(200, self.clock.get_time())
        if self.changing:
            self.changeLevel(self.currLevel.door.nextLevel,dT)
            return
        self.pc.update(dT)
        collisionCheck(self, self.playerGroup, self.currLevel)
        
        self.cam.update(self.player.rect)
        
        self.playerGroup.update(dT, self.currLevel)
        self.currLevel.enemies.update(dT, self.currLevel, self.player) # We shouldn't need to pass self.currLevel to a group that's owned by currLevel

        ##This is where the method for door collision and movement and level change happens 
        
        self.currLevel.ammo.update(dT, self.currLevel)

        
            
    
    def draw(self, screen):
        # draw
        if not self.changing:
            self.gameArea.fill((0,0,0))
            self.cam.draw_background(self.gameArea, self.currLevel.background)
            self.cam.draw_sprite(self.gameArea, self.player)
            self.cam.draw_sprite_group(self.gameArea, self.player.bullets)
            self.cam.draw_sprite_group(self.gameArea,self.player.meleeGroup)
            self.cam.draw_sprite_group(self.gameArea, self.currLevel.enemies)
            self.cam.draw_sprite_group(self.gameArea, self.currLevel.ammo)
            self.cam.draw_sprite_group(self.gameArea, self.currLevel.dirtyTiles)
        pygame.display.flip() # Refresh the screen
        
        self.gameHud.hudDraw(self.player.health)


if __name__ == "__main__":
    game = Game()
    game.run()

pygame.quit()
#print "Program complete"
