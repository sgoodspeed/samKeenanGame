from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw
from projectiles import *
from core.settings import *
from core.level import DirtyTile

from anim import Animation, AnimationFrames
from core.spritesheet import SpriteSheet

class PlayerAnimation(Animation):
    _rows = {"still": 0,
             "left": 2,
             "right": 1,
             "jump": 5,
             "hurt": (0,3)}

    def __init__(self, player, image, duration):
        self.player = player
        self.y = self._rows["still"]
    
        spritesheet = SpriteSheet(image, (2, 9), colorkey=(255,255,255))
        frames = [ (duration, 0),
                   (duration, 1)]

        Animation.__init__(self, spritesheet, frames)

    def update(self, dt):
        self.time += dt
        
        if self.player.thrown:
            self.x, self.y = self._rows["hurt"]
        else:
            if self.player.direction == 1:
                if self.player.jumping > 0:
                    self.x = self.get_frame_data(self.time) 
                    self.y = self._rows["jump"]
                else:
                    self.x = self.get_frame_data(self.time)
                    self.y = self._rows["right"]
            elif self.player.direction == -1:
                if self.player.jumping > 0:
                    self.x = self.get_frame_data(self.time) 
                    self.y = self._rows["jump"]
                else:
                    self.x = self.get_frame_data(self.time)
                    self.y = self._rows["left"]
            else:
                self.x = self.get_frame_data(self.time)
                self.y = self._rows["still"]

class Player(Sprite):
    vX = 0
    vY = 0
    jumping = 0
    decay = 0
    gravity = True
    melee = False
    
    def __init__(self):
        Sprite.__init__(self)
        self.thrown = False        
        self.direction = 1
        
        self.bullets = Group()
        self.meleeGroup = GroupSingle()
        self.ammo = 9001
        self.health = 100
        self.facing = 1
        self.timer = 0
        self.doorChange = False
        self.direction = None
        self.cleaning = False
        self.cleaningSlowdown = 1
        
        self.anim = PlayerAnimation(self, "mario", 80)
        self.image = self.anim.get_current_frame()
        self.rect = self.image.get_rect()
        
        self.cleanRect = Rect(self.rect.bottomleft, (10,10))

    def move(self, direction):
        self.vX = direction * PLAYER_SPEED * self.cleaningSlowdown # This doesn't actually MOVE anything, it just sets velocity
        if direction !=0:
            self.facing = self.direction

        self.direction = direction
        
    def jump(self):
        # Like move(), this doesn't actually do the jumping, it just sets up the variables and tells the player that it is now jumping. Update does the heavy lifting.
        self.vY = PLAYER_JUMP_SPEED
        self.jumping +=1

    def changeLevel(self, startCoords):
        #print startCoords, self.rect.bottomleft
        self.rect.bottomleft = startCoords
        self.vY = 0
        self.vX = 0
        self.jumping = 0
        self.bullets.empty()

    def touches(self, group):
        touching = Group()
        coll = self.rect
        for sprite in group:
            if coll.colliderect(sprite.rect):
                touching.add(sprite)
        return touching

    def update(self, dT, level):
        self.anim.update(dT)
        self.image = self.anim.get_current_frame()
        
        dT = dT / 1000.0
        self.dT = dT #For use in meleeAttack
        
        self.vY -= dT * GRAVITY_SPEED
        dX = self.vX * dT
        dY = -self.vY * dT

        self.bullets.update(dT, level)

        # update position
        prev_rect = self.rect
        self.rect = self.rect.move(dX, dY)
        
        self.rect.clamp_ip(level.bounds)  
        
        for sprite in self.touches(level.solidTiles):
            if isinstance(sprite, DirtyTile) and self.cleaning:
                sprite.clean()
                
            rect = sprite.rect 
            
            # collide with walls
            if (self.jumping == 0 and rect.top < self.rect.bottom-2) or (self.jumping > 0 and rect.top < self.rect.bottom):
                if self.rect.left <= rect.right and prev_rect.left >= rect.right:
                    self.rect.left = rect.right
                if self.rect.right >= rect.left and prev_rect.right <= rect.left:
                    self.rect.right = rect.left


            # handle cielings
            if rect.left < self.rect.right and self.rect.left < rect.right:
                if self.rect.top <= rect.bottom and prev_rect.top >= rect.bottom:
                    self.vY /= 2.0   # halve speed from hitting head
                    self.rect.top = rect.bottom

            # handle landing
            if self.rect.bottom >= rect.top and prev_rect.bottom <= rect.top:
                if self.thrown:
                    self.vX=0
                    self.thrown = False
                if self.jumping == 0 and not ((self.rect.left <= rect.right and prev_rect.left >= rect.right) or (self.rect.right >= rect.left and prev_rect.right <= rect.left)):
                    self.vY = 0
                    self.rect.bottom = rect.top
                    self.jumping = 0
                elif self.jumping > 0 and not ((self.rect.left <= rect.right and prev_rect.left >= rect.right) or (self.rect.right >= rect.left and prev_rect.right <= rect.left)):
                    self.jumping = 0
                    self.rect.bottom = rect.top

        self.cleanRect.topleft = self.rect.topleft
        
        if self.meleeGroup is not None:
            self.meleeGroup.update(dT)
                
                    
                    

                    
    def shoot(self):
        if self.ammo > 0:
            bullet = Sponge(self.rect.x, self.rect.y, self.facing, SPONGE_THROW_SPEED)
            self.bullets.add(bullet)
            self.ammo -= 1
            
            
    def meleeAttack(self):
        
        self.melee = True
        if self.melee:
            self.attack = MelRect(self)
            self.meleeGroup.add(self.attack)
            self.timer = 0

    def takeDamage(self,damageAmount):
        self.health-=damageAmount
        if self.health <=0:
            pass
