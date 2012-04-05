#!/usr/bin/env python
import os
import pygame
from pygame.locals import *

from core.input import InputManager, KeyListener, MouseListener
from world.player import *
from tiles import *
from pygame.sprite import *






# core/sound.py
class SoundManager(object):
    def play(self, which):
        pass
        #print "playing %s sound" % which


# controls/player.py
#3.  player controller, where we have our conditions of WHAT happens when WHAT key gets pressed.
class PlayerController(KeyListener, MouseListener):
    def __init__(self, player):
        self.player = player

    def on_keydown(self, event):
        if event.key == K_SPACE and self.player.jumping <2:
            self.player.jump()
#Note to future selves: You guys look handsome and you should figure out key repeat exemptions
        if event.key == K_LEFT:
            self.player.move(-1)
        if event.key == K_RIGHT:
            self.player.move(1)

    def on_keyup(self,event):
        if event.key == K_LEFT or event.key == K_RIGHT:
            self.player.vX = 0

    #def on_motion(self, event):
     #   self.player.move( event.rel )



# controls/sound.py
class SfxController(KeyListener):
    def __init__(self, sm, game):
        self.game = game
        self.sm = sm

    def on_keydown(self, event):
        if self.game.paused():
            return

        if event.key == K_SPACE:
            self.sm.play("jump")

        if event.key == K_c:
            self.sm.play("slash")



class Game(object):
    size = 800, 600
    fps = 30

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(100,100)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)

        self.input = InputManager()

        self.player = Player()
        self.playerGroup = pygame.sprite.GroupSingle(self.player)
        
        self.sounds = SoundManager()
        
        pc = PlayerController(self.player)
        self.input.add_key_listener(pc)
        self.input.add_mouse_listener(pc)

        sc = SfxController(self.sounds, self)
        self.input.add_key_listener(sc)

        self.img_tiles = load_image("tiles", (0,255,200))
        self.tilesheet = TileSheet(self.img_tiles, (32, 32))
        self.level = Level("test_level", self.tilesheet)
        
    def paused(self):
        return False


    def quit(self):
        self._done = True

    def run(self):
        self._done = False

        while not self._done:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                else:
                    self.input.handle_event(event)

            # update
            dT = self.clock.get_time()
            
            #self.playerGroup.update(dT)
            self.player.update(dT)
            
            
            # draw
            self.screen.fill((0,0,0))
            self.screen.blit(self.level.image,(0,0))
            self.playerGroup.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()

pygame.quit()
