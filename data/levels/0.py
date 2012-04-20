#! /usr/bin/env python

import pygame
from pygame.sprite import *
from world.enemies import *

def enemies():
    enemyGroup = Group()
    enemyGroup.add(sampleEnemy((50,50), (0,0,0)))
    return enemyGroup