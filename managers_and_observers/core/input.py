import pygame
from pygame.locals import *

class KeyListener(object):
    #1. which does nothing but exist to know what event has occured, which can be any key at all. Then PlayerController in main takes KeyListener as an argument, which lets us pass over any key that gets pressed to...(continued in main)
    def on_keydown(self, event): pass
    def on_keyup(self, event): pass


class MouseListener(object):
    def on_buttondown(self, event): pass
    def on_buttonup(self, event): pass
    def on_motion(self, event): pass

class InputManager(object):
    def __init__(self):
        #These are lists of all the events and key types, which start blank
        self._key = []
        self._mouse = []

    def add_mouse_listener(self, listener):
        #this is where buttons pressed are added to the lists, listener being 
        self._mouse.append(listener)

    def add_key_listener(self, listener):
        self._key.append(listener)

    def handle_event(self, event):
        #1. Here we check if a key is being pressed, at all. Then we pass the event type to key listener, 
        if event.type == KEYDOWN:
            for listener in self._key:
                listener.on_keydown(event)
        elif event.type == KEYUP:
            for listener in self._key:
                listener.on_keyup(event)
                
        elif event.type == MOUSEBUTTONDOWN:
            for listener in self._mouse:
                listener.on_buttondown(event)
        elif event.type == MOUSEBUTTONUP:
            for listener in self._mouse:
                listener.on_buttonup(event)
        elif event.type == MOUSEMOTION:
            for listener in self._mouse:
                listener.on_motion(event)
