#!/usr/bin/env python

import pygame
from pygame.locals import *
from ui import InfoText, InfoBlock
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
    start_key = K_SPACE
    restart_key = K_r
    
    paused_msg = "Press <Space> to resume."
    menu_msg = "Press <Space> to play!\nControls:\nArrow keys to move."
    gameover_msg = "GAAAAAAAME OVEEEEER FUCKING NEEEEERD!!1!"
    restart_msg = "Press <R> to restart."
    

    def __init__(self):
        pygame.init()
        # Screen init
        self.screen = pygame.display.set_mode(SCREEN_SIZE, self.SCREEN_FLAGS)
        
        # Subsurfaces
        self.hud = self.screen.subsurface(self.hudRect)
        self.gameArea = self.screen.subsurface(self.gameRect)
        
        # Set state
        self.state = "menu"

        #Clock
        self.clock = pygame.time.Clock()
        
        pygame.display.set_caption(TITLE)
        
        font = pygame.font.Font(None, 40)
        self.pause_text = InfoText(self.paused_msg, 40)
        self.gameover_text = InfoText(self.gameover_msg, 40)
        self.menu_text = InfoBlock(self.menu_msg, 40)
        self.restart_text = InfoText(self.restart_msg, 40, v_offset=50)
        
        #self.paused_text.set_colorkey((0,0,0))

        
        # Set bounds
        self.bounds = self.screen.get_rect()
        
        # Setup managers
        self.input = InputManager()
        self.sounds = SoundManager()       

    def quit(self):
        self.done = True

    def overlay(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0,0,0))
        overlay.set_alpha(100)
        self.screen.blit(overlay, (0,0))

    def quit_or_pause(self, events):
        for event in events:
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.quit()
            elif event.type == KEYDOWN and event.key == self.pause_key:
                if self.state == "play":
                    self.state = "paused"
            elif event.type == KEYDOWN and event.key == self.start_key:
                if self.state == "paused":
                    self.state = "play"

    
    def menu(self):        
        self.overlay()

        self.menu_text.draw(self.screen)
        
        self.quit_or_pause(self.events)

        for event in self.events:
            if event.type == KEYDOWN and event.key == self.start_key:
                self.state = "start_game"
                
    def start_game(self):
        self.setup_game()
        self.state = "play"
        
    def play(self):
        self.quit_or_pause(self.events)
        
        for event in self.events:
            self.input.handle_event(event) # Pass the event to the input manager, which will then pass it off to the appropriate controller.
        
        self.update()
        self.draw(self.screen)
        
    def pause(self):
        self.overlay()
        self.pause_text.draw(self.screen)
        self.quit_or_pause(self.events)

    def gameover(self):
        self.quit_or_pause(self.events)
        self.overlay()
        self.gameover_text.draw(self.screen)
        self.restart_text.draw(self.screen)
        
        for event in self.events:
            if event.type == KEYDOWN and event.key == self.restart_key:
                self.state = "menu"

    def step(self):
        self.clock.tick(FPS)
        self.events = pygame.event.get()

        if self.state == "menu":
            self.menu()
       
        if self.state == "start_game":
            self.start_game()
        
        if self.state == "play":
            # Pause if screen is hidden
            if not pygame.display.get_active() and not self.paused:
                self.state = "paused"
                return
            else:
                self.play()
        
        if self.state == "paused":
            self.pause()
        
        if self.state == "gameover":
            self.gameover()
        
        pygame.display.flip()
            
            


    def run(self):
        self.done = False
        self.clock = pygame.time.Clock()
        while not self.done:
            self.step()
            
    def setup_game(self): pass
    def update(self): pass
    def draw(self, screen): pass
