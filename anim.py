#! /usr/bin/env python

import pygame

class AnimationFrames(object):
    def __init__(self, frames, loops=-1):
        self._times = []
        self._data = []
        
        total = 0
        for t, data in frames:
            total += t
            self._times.append(total)
            self._data.append(data)
        
        self.end = total
        self.loops = loops
        
    def get(self, time):
        if self.loops == -1 or time < self.loops*self.end:
            time %= self.end
        if time > self.end:
            return self._data[-1]
        idx = 0
        while self._times[idx] < time:
            idx += 1
        
        return self._data[idx]
        
class Animation(object):
    def __init__(self, spritesheet, frames):
        if not isinstance(frames, AnimationFrames):
            frames = AnimationFrames(frames)
        self.spritesheet = spritesheet
        self.frames = frames
        self.time = 0
        self.update(0)
        
    def get_frame_data(self, t):
        return self.frames.get(t)
        
    def update(self, dt):
        self.time += dt
        self.x, self.y = self.get_frame_data(self.time)
    
    def get_current_frame(self):
        return self.spritesheet.get(self.x, self.y)