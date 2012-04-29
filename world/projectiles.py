import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import draw, Surface
from core.settings import *
from pickUp import Pickup


class Weapon(object):
    def hurt(self, enemy, level, player):
        if enemy not in self.hasHurt:
            self.hasHurt.append(enemy)
            enemy.takeDamage(self.damage, level)
            enemy.vY += ENEMY_THROWBACK
            enemy.direction = player.facing

# Generic Projectile Class
class Sponge(Pickup, Weapon):
    damage = SPONGE_DAMAGE
    def __init__(self, x, y, direction, vY):
        Pickup.__init__(self)
        self.direction = direction
        
        self.vX = self.direction * SPONGE_THROW_SPEED
        self.rect = Rect((x,y), SPONGE_SIZE)
        
        self.image = Surface(self.rect.size)
        draw.rect(self.image, (255,0,0), self.image.get_rect())
        self.vY = vY
        self.hasHurt = []

class MelRect(Sprite, Weapon):
    color = 0,0,255
    damage = MELEE_DAMAGE
    rectSize = MELEE_SIZE
    def __init__(self,player):
        Sprite.__init__(self)
        self.player = player
        #print self.facing
        if self.player.facing == 1:
            print "Facing right melee"
            self.rect = Rect(self.player.rect.midright,self.rectSize)
        elif self.player.facing == -1:
            print "Facing left melee"
            self.rect = Rect((self.player.rect.midleft[0]-self.rectSize[0],self.player.rect.midleft[1]),self.rectSize)
        else:
            print "No facing variable"
            self.player.facing = 1
            self.rect = Rect(self.player.rect.midright,self.rectSize)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, self.color, self.rect)
        self.timer = 0

        #Collision-y code stuff
        self.hasHurt = []
    def update(self,dT):
        self.timer+=dT
        if self.player.facing == 1:
            self.rect.midleft = self.player.rect.midright
        elif self.player.facing == -1:
            self.rect.midright = self.player.rect.midleft
        
        self.rect.midleft
        #print self.timer
        if self.timer > .40:
            self.kill()


        
        
        
