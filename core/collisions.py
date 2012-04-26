import pygame

from enemies import *
from world.player import *
from level import *
from pygame.sprite import *
from core.settings import *

def collisionCheck(game,player,level):
    for enemy in groupcollide(level.enemies, player, False, False):
        if player.sprite.vX != 0:
            player.sprite.vX = player.sprite.direction*PLAYER_SPEED*-1.5
        else:
            player.sprite.vX = enemy.direction*PLAYER_SPEED*1.5
        player.sprite.vY = 300
        player.sprite.takeDamage(enemy.damage)
        player.sprite.thrown = True
        
    
    for enemy in groupcollide(level.enemies, player.sprite.bullets, False, True):
        enemy.takeDamage(BULLET_DAMAGE, level)

    for ammo in groupcollide(level.ammo, player, True, False):
        player.sprite.ammo += AMMO_AMOUNT
     
    for melee, enemies in groupcollide(player.sprite.meleeGroup, level.enemies, False,False).items():
        for enemy in enemies:
            melee.hurt(enemy, level)

    if level.door.rect.colliderect(player.sprite.rect) and player.sprite.doorChange:
        game.changing = True
        
