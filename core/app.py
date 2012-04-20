#!/usr/bin/env python

import pygame
from pygame.locals import *
from ui import InfoText
from core.input import InputManager, KeyListener, MouseListener
from core.settings import *

# core/sound.py
class SoundManager(object):
    def play(self, which):
        pass

class Application(object):
    hudRect = ((0,0,SCR_W,HUD_HEIGHT))
    gameRect = ((0,40,SCR_W,SCR_H-HUD_HEIGHT))
    SCREEN_FLAGS = DOUBLEBUF|HWSURFACE|SRCALPHA
    pause_key = K_p
    paused_text = "Press Space to Resume"
    restart_key = K_r
    gameover_msg = "Game Over!"
    is_gameover = False


    def __init__(self):
        pygame.init()
        #Scree init
        self.screen = pygame.display.set_mode(SCREEN_SIZE, self.SCREEN_FLAGS)
        #Subsurfaces
        self.hud = self.screen.subsurface(self.hudRect)
        
        self.gameArea = self.screen.subsurface(self.gameRect)

        

        #Clock
        self.clock = pygame.time.Clock()
        
        pygame.display.set_caption(TITLE)
        
        font = pygame.font.Font(None, 40)
        self._paused_text = font.render(self.paused_text, True, (255,255,255), (0,0,0))
        self._paused_text.set_colorkey((0,0,0))

        self.paused = False
        self.bounds = self.screen.get_rect()
        self.gameover_text = InfoText(self.gameover_msg, 40)
        
        # Setup managers
        self.input = InputManager()
        self.sounds = SoundManager()

    def pause(self):
        self.paused = True
        self.on_pause()
        self._draw_pause()

    def _draw_pause(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        self.screen.blit(overlay, (0,0))

        loc = self._paused_text.get_rect()
        loc.center = self.screen.get_rect().center
        self.screen.blit(self._paused_text, loc)
        pygame.display.flip()
    
    def do_gameover(self):
        self.is_gameover = True

        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        self.screen.blit(overlay, (0,0))

        self.gameover_text.draw(self.screen)
        pygame.display.flip()


    def resume(self):
        self.paused = False
        self.on_resume()

    def quit(self):
        self.done = True

    def step(self):
        self.clock.tick(FPS)

        # Pause if screen is hidden
        if not pygame.display.get_active() and not self.paused:
            self.pause()

        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.quit()
            elif event.type == KEYDOWN and event.key == self.pause_key and not self.is_gameover:
                if self.paused:
                    self.resume()
                else:
                    self.pause()
            else:
                self.input.handle_event(event) #Otherwise, pass the event to the input manager, which will then pass it off to the appropriate controller.

         # update if not paused
        if not self.paused and not self.is_gameover:
            self.update()
            self.draw(self.screen)
            pygame.display.flip()
            


    def run(self):
        self.done = False
        self.clock = pygame.time.Clock()
        self.on_start()
        while not self.done:
            self.step()
        self.on_quit()       
            
    def update(self): pass
    def draw(self, screen): pass

    def on_resume(self): pass
    def on_pause(self): pass
    def on_start(self): pass
    def on_quit(self): pass
