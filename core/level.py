#! /usr/bin/env python
import os

from pygame.locals import *
from pygame.sprite import *
from pygame import Surface,Rect
from core.settings import *
from enemies import *
from world.door import Door

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
            enemyClass = globals()[enemyType]((x,y))
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

class DirtyTile(Tile):
    def __init__(self, tileImage, cleanImage, x, y, tileType):
        Tile.__init__(self, tileImage, True, x, y, tileType)
        self.cleanImage = cleanImage
        self.cleaned = False

    def clean(self):
        if not self.cleaned:
            self.cleaned = True
            self.image = self.cleanImage        
        


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
        dirtyTileGroup = Group()
        doorGroup = Group()

        
        # Loop through the .lvl file
        for y, row in enumerate(data):
            tileOffset = 0
            if row == "EOL":
                break
            for x, cell in enumerate(row):
                if cell.isdigit():
                    tileOffset += self.w
                # Get the image that corresponds to this cell
                tileImage = self.tilemap.get(cell)
                if tileImage:
                    isSolid = cell in TILE_SOLIDS # If the cell is in the solid list then it should be solid
                    if cell in DIRTY_TILES:
                        cleanCoord = DIRTY_TILES_CLEAN[cell]
                        cleanImage = self.tilemap.get(cleanCoord)
                        tile = DirtyTile(tileImage, cleanImage, x*self.w-tileOffset, y*self.h, cell) # We need to assign a secondary image here where it says tileImage the second time that will display when it's cleaned
                        dirtyTileGroup.add(tile)
                    else:
                        if cell == "o": # o = door
                            nextLevel = row[x+1]
                            door = Door(nextLevel, (x*self.w-tileOffset, y*self.h))
                            doorGroup.add(door)
                        tile = Tile(tileImage, isSolid, x*self.w-tileOffset, y*self.h, cell)
                    if isSolid:
                        solidTileGroup.add(tile)
                    tileGroup.add(tile) # Create a Tile object with the correct image
        return tileGroup, solidTileGroup, dirtyTileGroup, size, doorGroup
        
# Level class
# This holds the actual final rendered image of the level according to the .lvl file, rendered with tiles from the tilemap image
class Level(object):
    def __init__(self, name, tilesheet, index):
        path = os.path.join("data", "levels", name) + ".lvl"
        f = open(path, "r")
        data = f.read().replace("\r", "").strip().split("\n")
        f.close()
        
        self.index = index	
        self.doors = []
        self.name = name
        self.tiles, self.solidTiles, self.dirtyTiles, size, self.doors = tilesheet.render(data)
        self.bounds = Rect((0,0), size)
        
        self.enemies = createEnemies(data)

        self.ammo = Group()
        
        self.render_background()
        
    def render_background(self):
        self.background = Surface(self.bounds.size)
        self.tiles.draw(self.background)
        self.doors.draw(self.background)
        
    def getStartPos(self, prevLevel):
        for door in self.doors:
            if int(door.nextLevel) == int(prevLevel):
                return door.rect.bottomleft



