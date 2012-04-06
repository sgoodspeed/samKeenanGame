import pygame
from pygame.locals import *

# These are just prototype classes, which we will use later
class KeyListener(object):
    def on_keydown(self, event): pass
    def on_keyup(self, event): pass

class MouseListener(object):
    def on_buttondown(self, event): pass
    def on_buttonup(self, event): pass
    def on_motion(self, event): pass

# This is what deals with all the Input to the game. All input goes through the input manager, which then passes each input event to each of the listeners that it has.
class InputManager(object):
    def __init__(self):
        # These are lists of all listeners in the manager
        self._key = []
        self._mouse = []

    def add_mouse_listener(self, listener):
        # This just adds a mouse listener to the InputManager
        self._mouse.append(listener)

    def add_key_listener(self, listener):
        # And this adds a key listener
        self._key.append(listener)

    def handle_event(self, event):
        # All events are passed to this method, which then passes the event to the correct method for each listener
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
