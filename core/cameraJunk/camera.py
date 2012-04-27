"""
camera.py

"""

from pygame import Rect

from util import rel_rect

class Camera(object):

    def __init__(self, target, bounds, size):
        self.bounds = bounds
        self.rect = Rect((0,0), size)

    def update(self, target):
        self.rect.center = target.center
        self.rect.clamp_ip(self.bounds)

    def draw_background(self, surf, bg):
        surf.blit(bg, (-self.rect.x, -self.rect.y))

    def draw_background_alpha(self, surf, bg, alpha):
        new_bg = bg.copy()
        new_bg.set_alpha(alpha)
        surf.blit(new_bg, (-self.rect.x, -self.rect.y))

    def draw_sprite(self, surf, sprite):
        if self.rect.colliderect(sprite.rect):
            surf.blit(sprite.image, rel_rect(sprite.rect, self.rect))
            
    def draw_sprite_group(self, surf, group):
        for sprite in group:
            if self.rect.colliderect(sprite.rect):
                surf.blit(sprite.image, rel_rect(sprite.rect, self.rect))
    
    def draw_sprite_group_alpha(self, surf, group, alpha):
        for sprite in group:
            if self.rect.colliderect(sprite.rect):
                new_sprite = sprite.image.copy()
                new_sprite.set_alpha(alpha)
                surf.blit(new_sprite, rel_rect(sprite.rect, self.rect))

    def draw_sprite_alpha(self, surf, sprite, alpha):
        if self.rect.colliderect(sprite.rect):
            new_sprite = sprite.image.copy()
            new_sprite.set_alpha(alpha)
            surf.blit(new_sprite, rel_rect(sprite.rect, self.rect))
