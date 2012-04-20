### APP
SCREEN_SIZE = SCR_W, SCR_H = 800, 600
TITLE = "Ghosts 'n' Gears" #Haha I still think this title is hilarious
FPS = 30
HUD_HEIGHT = 40

### TILES
TILE_SIZE = T_W, T_H = 32, 32
TILE_MAP_COORDS = { "~": (395,236),
                    "%": (385,289),
                    ".": (192,96),
                    "&": (32,32),
                    "o": (0,0)
                    }
TILE_SOLIDS = [ ".", 
                "&", 
                "%"
                ]

### PLAYER
PLAYER_SIZE = PLY_W, PLY_H = T_W*.75, T_H*.75
PLAYER_START = PLAYER_START_X, PLAYER_START_Y = 100, 504
PLAYER_SPEED = 200
PLAYER_JUMP_SPEED = 300
PLAYER_MAX_JUMPS = 2
GRAVITY_SPEED = 600

##RAT VARIABLES
RAT_SIZE = (T_W*1.5, T_H*1.5)
RAT_SPEED = 150
RAT_DAMAGE = 15
RAT_HEALTH = 30


### PROJECTILES
BULLET_SIZE = PLY_W*2, PLY_H
BULLET_SPEED = 400
BULLET_DAMAGE = 10

### PICKUPS
AMMO_SIZE = (T_W*.4, T_H*.4)
PICKUP_THROW_SPEED = 50
AMMO_AMOUNT = 15

### MAIN
## How this works: 
#    level 0 links to level 1 
#    level 1 links to level 2
#    etc.
LEVELS =      ["0","1","2"]
LEVEL_LINKS = [1, 2, 0]
TILEMAP_IMAGE = "tiles"
