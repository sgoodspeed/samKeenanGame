### APP
SCREEN_SIZE = SCR_W, SCR_H = 800, 600
TITLE = "Ghosts 'n' Gears" #Haha I still think this title is hilarious
FPS = 20
HUD_HEIGHT = 40

### TILES
TILE_SIZE = T_W, T_H = 32, 32
TILE_MAP_COORDS = { "~": (160,0),  # Red wall
                    ".": (0,33),  # Stone floor
                    "&": (64,0), # Window
                    "o": (0,255), # Door (closed)
                    "D": (32,255), # Door (open)
                    ",": (128,32), # Wood floor w/ Ectoplasm
                    "/": (0,0), # Wood floor cleaned
                    }
TILE_SOLIDS = [ ".",  
                ",",
                "/"
                ]

DIRTY_TILES = [","]

DIRTY_TILES_CLEAN = {",": "/"}

DOOR = "o"
OPENDOOR = "D"

### PLAYER
PLAYER_SIZE = PLY_W, PLY_H = T_W, T_H*2.2
PLAYER_START = PLAYER_START_X, PLAYER_START_Y = 100, 504
PLAYER_SPEED = 200
PLAYER_JUMP_SPEED = 300
PLAYER_MAX_JUMPS = 2
GRAVITY_SPEED = 600
CLEAN_SLOWDOWN = .5

### SPONGES
SPONGE_THROW_SPEED = 200
SPONGE_SIZE = (T_W*.4, T_H*.4)
SPONGE_DAMAGE = 10
ENEMY_THROWBACK = 200


### ATTACKS
BULLET_SIZE = PLY_W*2, PLY_H
BULLET_SPEED = 400
BULLET_DAMAGE = 10

MELEE_DAMAGE = 15
MELEE_SIZE = (100,10)

##RAT VARIABLES
RAT_SIZE = (T_W*1.5, T_H*1.5)
RAT_SPEED = 150
RAT_DAMAGE = 15
RAT_HEALTH = 30
RAT_WEIGHT = 1

##Frank's Variables
FRANK_SIZE = (T_W*.8, T_H*1)
FRANK_SPEED = 100
FRANK_DAMAGE = 30
FRANK_HEALTH = 50
FRANK_BOUNDS = 250
FRANK_JUMP_DIST = 150
FRANK_WEIGHT = .5

#GOBLIN VARIABLES
GOB_SIZE = (T_W*.8, T_H*1.8)
GOB_SPEED = 80
GOB_DAMAGE = 40
GOB_HEALTH = 50
GOB_BOUNDS = 250
GOB_WEIGHT = 1
GOB_ATTACK_DIST = MELEE_SIZE[0]+(GOB_SIZE[0]/2)


#GHOST VARIABLES
GHOST_SIZE = (50, 70)
GHOST_SPEED = 100
GHOST_DAMAGE = 20
GHOST_HEALTH = 20
GHOST_BOUNDS = 500
GHOST_ATTACK_DIST = 400

### ATTACKS
BULLET_SIZE = PLY_W*2, PLY_H
BULLET_SPEED = 400
BULLET_DAMAGE = 10

MELEE_DAMAGE = 15
MELEE_SIZE = (100,10)


### PICKUPS
AMMO_SIZE = (T_W*.4, T_H*.4)
PICKUP_THROW_SPEED = 50
AMMO_AMOUNT = 1

### MAIN
## How this works: 
#    level 0 links to level 1 
#    level 1 links to level 2
#    etc.
LEVELS =      ["0","1","2"]
TILEMAP_IMAGE = "tiles"
