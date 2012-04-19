import pygame

from enemies import *
from world.player import *
from level import *
from pygame.sprite import *
from core.settings import *

def collisionCheck(player,enemyGroup):
    for enemy in groupcollide(enemyGroup, player, False, False):
        player.sprite.rect.x+= enemy.direction *20
        player.sprite.takeDamage(enemy.damage)
        
    
    for enemy in groupcollide(enemyGroup, player.sprite.bullets, False, True):
        enemy.takeDamage(BULLET_DAMAGE)