import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw
from world.pickUp import *
from core.settings import *
from random import *
import math
from anim import Animation, AnimationFrames
from core.spritesheet import SpriteSheet
from world.projectiles import Sponge,MelRect

class Enemy(Sprite):
    vY = 0
    vX = 0
    
    def __init__(self, startPos):
        Sprite.__init__(self)
        self.direction = randrange(-1,2,2)
        self.startPos = startPos
        self.onGround = False
        self.timer = 0
        self.dying = False
        self.directed = False

    def touches(self, group):
        touching = Group()
        coll = self.rect
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching

    def update(self, dT, level, player):
        self.move(dT, level, player)
        self.collide(level)

    def move(self, dT, level, player):
        if self.dying:
            self.die(level, dT)
        else:
            self.distance = self.getDistance(player.rect.center)
        
            self.vX = self.direction * self.speed # This doesn't actually MOVE anything, it just sets velocity
        
        dT = dT / 1000.0
    
        self.vY -= dT * (GRAVITY_SPEED * self.weight)
        dX = self.vX * dT
        dY = -self.vY * dT
    
        # update position
        self.prev_rect = self.rect
        #print dX,dY
        self.rect = self.rect.move(dX, dY)
        if self.rect.x < 0 or self.rect.x > level.bounds.right:
            self.direction*=-1
        self.rect.clamp_ip(level.bounds)   # temp error

    def collide(self, level):
        # update position
        for sprite in self.touches(level.solidTiles):
            rect = sprite.rect 
        
            # collide with walls
            if (rect.top < self.rect.bottom-2):
                if self.rect.left <= rect.right and self.prev_rect.left >= rect.right:
                    self.rect.left = rect.right+1
                    self.direction *=-1
                    self.directed = True
                
                if self.rect.right >= rect.left and self.prev_rect.right <= rect.left:
                    self.rect.right = rect.left-1
                    self.direction *=-1
                    self.directed = True
                
            # handle cielings
            #if rect.left < self.rect.right and self.rect.left < rect.right:
             #   if self.rect.top <= rect.bottom and prev_rect.top >= rect.bottom:
              #      self.vY /= 2.0   # halve speed from hitting head
               #     self.rect.top = rect.bottom

            # handle landing
            self.onGround = False
            if self.rect.bottom >= rect.top and self.prev_rect.bottom <= rect.top:
                if not ((self.rect.left <= rect.right and self.prev_rect.left >= rect.right) or (self.rect.right >= rect.left and self.prev_rect.right <= rect.left)):
                    self.vY = 0
                    self.rect.bottom = rect.top
                    self.onGround = True
                    if self.dying:
                        self.vX = 0                    
                
    def takeDamage(self, damageAmount, level):
        self.health-=damageAmount
        if self.health <=0:
            self.die(level)
            
    def getDistance(self,playerPos):
        x1,y1 = self.rect.center
        x2,y2 = playerPos
        #d = math.sqrt((x2-x1)**2 + (y2 - y1)**2)
        d = ((x2-x1) + (y2 - y1))
        #print d
        return d
        
    def die(self, level, dT=0):
        if not self.dying:
            self.dying = True
            level.ammo.add(Sponge(self.rect.right,self.rect.top, self.direction, SPONGE_THROW_SPEED)
        self.timer += dT
        if self.timer > 1500:
            self.kill()
        
class RatAnimation(Animation):
    _rows = {"left": 0,
             "right": 1,
             "dead": 2}

    def __init__(self, rat, image, duration):
        self.rat = rat
        self.y = self._rows["left"]
    
        spritesheet = SpriteSheet(image, (2, 3), colorkey=(0,255,0))
        frames = [ (duration, 0),
                   (duration, 1)]

        Animation.__init__(self, spritesheet, frames)

    def update(self, dt):
        self.time += dt
        
        if self.rat.dying:
            self.x = 0
            self.y = self._rows["dead"]
        else:
            if self.rat.direction == 1:
                    self.x = self.get_frame_data(self.time)
                    self.y = self._rows["right"]
            elif self.rat.direction == -1:
                    self.x = self.get_frame_data(self.time)
                    self.y = self._rows["left"]
    
class Rat(Enemy):
    damage = RAT_DAMAGE
    health = RAT_HEALTH
    size = RAT_SIZE
    speed = RAT_SPEED
    weight = RAT_WEIGHT
    
    def __init__(self, startPos):
        Enemy.__init__(self, startPos)
        self.anim = RatAnimation(self, "rat", 160)
        self.image = self.anim.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.center = self.startPos
        
    def update(self, dT, level, player):
        self.anim.update(dT)
        self.image = self.anim.get_current_frame()
        Enemy.update(self, dT, level, player)




class FrankAnimation(Animation):
    _rows = {"right": 0,
             "left": 1,
             "jump": 2,
             "hurt": 3,
             "dead": 4}

    def __init__(self, enemy, image, duration):
        self.enemy = enemy
        self.y = self._rows["left"]
    
        spritesheet = SpriteSheet(image, (3, 5), colorkey=(0,255,0))
        frames = [ (duration, 0),
                   (duration, 1)]

        Animation.__init__(self, spritesheet, frames)

    def update(self, dt):
        self.time += dt
        
        if self.enemy.state == "roaming":
            if self.enemy.direction == 1:
                self.x = self.get_frame_data(self.time)
                self.y = self._rows["right"]
            else:
                self.x = self.get_frame_data(self.time)
                self.y = self._rows["left"]
        elif self.enemy.state == "crouching":
            self.x = 0
            self.y = self._rows["jump"]
        elif self.enemy.state == "jumping" or self.enemy.state == "falling":
            self.x = 1
            self.y = self._rows["jump"]
            
        if self.enemy.dying:
            self.x = 0
            self.y = self._rows["dead"]
class Frank(Enemy):
    damage = FRANK_DAMAGE
    health = FRANK_HEALTH
    size = FRANK_SIZE
    speed = FRANK_SPEED
    boundSize = FRANK_BOUNDS
    weight = FRANK_WEIGHT

    def __init__(self, startPos):
        Enemy.__init__(self, startPos)
        self.timer = 0
        self.state = "roaming"
        self.attacking = False
        
        self.anim = FrankAnimation(self, "frank", 160)
        self.image = self.anim.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.center = self.startPos
        
        self.leftBound = self.rect.left - self.boundSize
        self.rightBound = self.rect.right + self.boundSize
    def update(self, dT, level, player):
        self.anim.update(dT)
        self.image = self.anim.get_current_frame()
        if self.state == "roaming":
            Enemy.update(self, dT, level, player)
            if self.rect.left<self.leftBound:
                self.direction*=-1
            if self.rect.right>self.rightBound:
                self.direction*=-1
            if self.jumpAttackCheck():
                self.state = "crouching"

        if self.state == "crouching":
            self.distance = self.getDistance(player.rect.center)
            
            self.timer+=dT
            if self.timer > 1000:
                self.state = "jumping"
            if self.distance > FRANK_JUMP_DIST*2:
                self.state = "roaming"

        if self.state == "jumping":
            self.onGround = False
            if self.distance != 0:
                self.direction = self.distance / abs(self.distance)
            self.vY = 180
            Enemy.update(self, dT, level, player)
            self.state = "falling"

        if self.state == "falling":
            Enemy.update(self, dT, level, player)
            if self.onGround:
                self.timer = 0
                self.leftBound = self.rect.left - self.boundSize
                self.rightBound = self.rect.right + self.boundSize
                self.state = "roaming"
            

    def jumpAttackCheck(self):
        #print self.distance
        if abs(self.distance) < FRANK_JUMP_DIST and self.onGround:
            return True
        else:
            return False
            

class Goblin(Enemy):
    damage = GOB_DAMAGE
    health = GOB_HEALTH
    size = GOB_SIZE
    speed = GOB_SPEED
    boundSize = GOB_BOUNDS
    weight = GOB_WEIGHT
    attackDist = GOB_ATTACK_DIST
    meleeGroup = Group()

    def __init__(self, startPos):
        Enemy.__init__(self, startPos)
        self.melee = False
        
        self.rect = Rect(startPos, (32,32))
        self.image = Surface(self.rect.size)
        self.rect.center = self.startPos
        
        self.leftBound = self.rect.left - self.boundSize
        self.rightBound = self.rect.right + self.boundSize
        
        self.timer = 0
        self.state = "roaming"
        self.attacking = False
        self.pick = 0
        self.attackTimer = 0
        self.rush = False


    def update(self, dT, level, player):
        self.timer += dT
        
        
        
        if self.timer >3000:
            self.pick = randrange(0,3)
            #print self.pick
            self.directed = False
            self.timer = 0
        if self.pick == 0:
            self.pause()
            self.timer
        elif self.pick == 1:
            self.moveRight()
        elif self.pick == 2:
            self.moveLeft()
        Enemy.update(self,dT,level,player)
        self.facing = self.direction
        
        if abs(self.distance) <200:
            if not self.rush:
                self.speed*=2
                self.rush = True
        if self.rush and abs(self.distance) >200:
            self.speed = GOB_SPEED
            self.rush = False
            
                    
    def moveLeft(self):
        if not self.directed:
           self.direction = -1
        

    def moveRight(self):
        if not self.directed:
            self.direction = 1

    def pause(self):
        if not self.directed:
            self.direction = 0
##
##class Ghost(Enemy):
##    damage = GHOST_DAMAGE
##    health = GHOST_HEALTH
##    size = GHOST_SIZE
##    speed = GHOST_SPEED
##    boundSize = GHOST_BOUNDS
##    attackDist = GHOST_ATTACK_DIST
##
##    def __init__(self, startPos):
##        Enemy.__init__(self, startPos)
##        self.boundsLeft = 
##        #self.anim = GhostAnimation(self, "ghost", 160)
##        #self.image = self.anim.get_current_frame()
##        self.rect = self.image.get_rect()
##        self.rect.center = self.startPos
##        
##    def update(self,startpos):
##        
##        self.move(dT, level, player)

    

   
