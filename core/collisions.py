import pygame

from enemies import *
from world.player import *
from level import *
from pygame.sprite import *
from core.settings import *

def collisionCheck(player,enemyGroup, ammoGroup, level):
    for enemy in groupcollide(enemyGroup, player, False, False):
        if player.sprite.vX != 0:
            player.sprite.vX = player.sprite.direction*PLAYER_SPEED*-1.5
        else:
            player.sprite.vX = enemy.direction*PLAYER_SPEED*1.5
        player.sprite.vY = 300
        player.sprite.takeDamage(enemy.damage)
        player.sprite.thrown = True
        
    
    for enemy in groupcollide(enemyGroup, player.sprite.bullets, False, True):
        enemy.takeDamage(BULLET_DAMAGE, level)

    for ammo in groupcollide(ammoGroup, player, True, False):
        player.sprite.ammo += AMMO_AMOUNT
     
    for melee, enemies in groupcollide(player.sprite.meleeGroup, enemyGroup, False,False).items():
        for enemy in enemies:
            melee.hurt(enemy, level)
