#! /usr/bin/env python
import os

import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect,draw
from core.settings import *
from enemies import *

# This just loads the tilemap image from data/images/[name].bmp
def load_image(name, colorkey=None):
    path = os.path.join("data", "images", name) + ".bmp"

    image = pygame.image.load(path).convert()
    if colorkey:
        image.set_colorkey(colorkey)
    return image


def createEnemies(data):
    enemiesGroup = Group()
    atEnd = False
    
    for y, row in enumerate(data):
        if row == "EOL":
            atEnd = True
        if atEnd and row != "EOL":
            lineData = row.split(" ")
            enemyType = str(lineData[0])
            x = int(lineData[1])
            y = int(lineData[2])
            enemyClass = eval(enemyType + "((x,y))")
            enemiesGroup.add(enemyClass)
    
    return enemiesGroup
            

## Tile class
class Tile(Sprite):
    def __init__(self, tileImage, isSolid, x, y, tileType):
        Sprite.__init__(self)
        self.isSolid = isSolid
        self.image = tileImage
        self.rect = tileImage.get_rect()
        self.rect.topleft = (x,y)
        self.tileType = tileType


## Tilesheet class
class TileSheet(object):
    def __init__(self, image, size):
        self.image = image # This is the tilemap image
        self.w,self.h = size # The size of each tile
        
        # Build a dictionary that pairs characters with tiles in the tilemap
        self.tilemap = {}
        for tile,coord in TILE_MAP_COORDS.items():
            if coord:
                x,y = coord
                self.tilemap[tile] = image.subsurface(x, y, self.w, self.h)

    def render(self, data):
        # create level image
        # Data is the .lvl file
        rows = len(data)
        cols = len(data[0])
        size = (cols * self.w, rows * self.h) # The size of the level is the number of rows and cols in the .lvl file times the height and width of each tile
        tileGroup = Group()
        solidTileGroup = Group()
        
        # Loop through the .lvl file
        for y, row in enumerate(data):
            if row == "EOL":
               break
            for x, cell in enumerate(row):
                # Get the image that corresponds to this cell
                tileImage = self.tilemap.get(cell)
                if tileImage:
                    isSolid = cell in TILE_SOLIDS # If the cell is in the solid list then it should be solid
                    if cell == "o": # o = door
                        doorLoc = x*self.w, y*self.h
                    tile = Tile(tileImage, isSolid, x*self.w, y*self.h, cell)
                    if isSolid:
                        solidTileGroup.add(tile)
                    tileGroup.add(tile) # Create a Tile object with the correct image
        return tileGroup, solidTileGroup, size, doorLoc
        
# Level class
# This holds the actual final rendered image of the level according to the .lvl file, rendered with tiles from the tilemap image
class Level(object):
    def __init__(self, name, tilesheet):
        path = os.path.join("data", "levels", name) + ".lvl"
        f = open(path, "r")
        data = f.read().replace("\r", "").strip().split("\n")
        f.close()
                
        self.name = name
        self.tiles, self.solidTiles, size, self.doorLoc = tilesheet.render(data)
        self.bounds = Rect((0,0), size)
        
        self.enemies = createEnemies(data)

        self.ammo = Group()
        
    def render_background(self):
        self.background = Surface(self.bounds.size)
        self.tiles.draw(self.background)
        self.door.draw(self.background)
        
    def addDoor(self, door):
        self.door = door
        self.door.rect.topleft = self.doorLoc
        self.render_background()







############## This is just example code, we don't use anything from here down #############
## Main Game
def main():
    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    pygame.key.set_repeat(50,50)

    # init game
    img_tiles = load_image("tiles", (0,255,200))
    tilesheet = TileSheet(img_tiles, (32, 32))
    level = Level("test_level", tilesheet)
    off_x, off_y = 0, 0

    # game loop
    done = False
    clock = pygame.time.Clock()
    while not done:
        # input
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True

            # move the camera
            elif event.type == KEYDOWN and event.key == K_LEFT:
                off_x += 5
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                off_x -= 5
            elif event.type == KEYDOWN and event.key == K_UP:
                off_y += 5
            elif event.type == KEYDOWN and event.key == K_DOWN:
                off_y -= 5

        # update

        # draw
        screen.fill((80,80,80))
        screen.blit(level.image, (off_x, off_y))

        # tick
        pygame.display.flip()
        clock.tick(30)
# main
if __name__ == "__main__":
    main()
    print "ByeBye"

pygame.quit()
