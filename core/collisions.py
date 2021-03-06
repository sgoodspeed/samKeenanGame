from pygame.sprite import *
from core.settings import *
from enemies import *


def collisionCheck(game,player,level):
    for enemy in groupcollide(level.enemies, player, False, False):
        if not enemy.dying:
            if player.sprite.vX != 0:
                player.sprite.vX = -player.sprite.direction * (PLAYER_SPEED*1.2)
            else:
                player.sprite.vX = enemy.direction * (PLAYER_SPEED*1.2)
            player.sprite.vY = 300
            player.sprite.takeDamage(enemy.damage)
            player.sprite.thrown = True
            if isinstance(enemy,Frank):
                enemy.direction*=-1
        
    
    for sponge, enemies in groupcollide(player.sprite.bullets, level.enemies, False, False).items():
        for enemy in enemies:
            if not sponge.hasBounced:
                sponge.hurt(enemy, level, player.sprite)

    for sponge in groupcollide(player.sprite.bullets, player, False, False):
        if sponge.hasBounced:
            player.sprite.ammo += AMMO_AMOUNT
            sponge.kill()
            
     
    for melee, enemies in groupcollide(player.sprite.meleeGroup, level.enemies, False,False).items():
        for enemy in enemies:
            melee.hurt(enemy, level, player.sprite)
    
    if player.sprite.doorChange:
        for door, player in groupcollide(level.doors, player, False, False).items():
            tilesReady = True
            for tile in level.dirtyTiles:
                if not tile.cleaned:
                    tilesReady = False
                    break
            if len(level.enemies) == 0 and tilesReady:                     
                game.nextLevel = door.nextLevel
                door.open()
                game.changing = True
        
