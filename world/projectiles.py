import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import draw, Surface
from core.settings import *


# Generic Projectile Class
class Bullet(Sprite):
    color = 255,0,0
    damage = BULLET_DAMAGE
    def __init__(self, x, y, dirX, dirY):
        Sprite.__init__(self)
        self.rect = Rect((x, y), BULLET_SIZE)
        self.image = Surface(self.rect.size)
        draw.rect(self.image, self.color, self.rect)
        self.dirY = dirY
        self.dirX = dirX
    
    def update(self, dT, level):        
        dY = int(self.dirY*BULLET_SPEED*dT)
        self.rect.y -= dY
        
        dX = int(self.dirX*BULLET_SPEED*dT)
        self.rect.x+=dX
        
        # Kill if we hit a solid tile
        if spritecollideany(self, level.solidTiles):
            self.kill()
        
        # Kill if we're out of the level
        if not level.bounds.contains(self.rect):
            self.kill()

class MelRect(Sprite):
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
    def hurt(self, enemy, level):
        if enemy not in self.hasHurt:
            self.hasHurt.append(enemy)
            enemy.takeDamage(MELEE_DAMAGE, level)


        
        
        
