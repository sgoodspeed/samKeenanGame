from pygame.sprite import *
from core.settings import *
from enemies import *


def collisionCheck(game,player,level):
    for enemy in groupcollide(level.enemies, player, False, False):
        if player.sprite.vX != 0:
            player.sprite.vX = -player.sprite.direction * (PLAYER_SPEED*1.2)
        else:
            player.sprite.vX = enemy.direction * (PLAYER_SPEED*1.2)
        player.sprite.vY = 300
        player.sprite.takeDamage(enemy.damage)
        player.sprite.thrown = True
        if isinstance(enemy,Frank):
            enemy.direction*=-1
        
    
    for enemy in groupcollide(level.enemies, player.sprite.bullets, False, True):
        enemy.takeDamage(BULLET_DAMAGE, level)

    for ammo in groupcollide(level.ammo, player, True, False):
        player.sprite.ammo += AMMO_AMOUNT
     
    for melee, enemies in groupcollide(player.sprite.meleeGroup, level.enemies, False,False).items():
        for enemy in enemies:
            melee.hurt(enemy, level)
    
    if player.sprite.doorChange:
        for door, player in groupcollide(level.doors, player, False, False).items():
         game.nextLevel = door.nextLevel
         game.changing = True
        
