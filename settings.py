# различные переменные для настройки игры, сделаю так, чтобы из файла брались
import math

# game settings
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
PENTA_HEIGHT = 5 * HEIGHT
DOUBLE_HEIGHT = 2 * HEIGHT
FPS = 60
TILE = 100
FPS_POS = (WIDTH - 65, 5)

# minimap settings
MINIMAP_SCALE = 5
MINIMAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_SCALE = 2 * MINIMAP_SCALE # 1 -> 12 x 8, 2 -> 24 x 16, 3 -> 36 x 24
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MINIMAP_SCALE)

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# sprite settings
DOUBLE_PI = math.pi * 2
CENTER_RAY = NUM_RAYS // 2 - 1
FAKE_RAYS = 100
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS

# texture settings (1200 x 1200)
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
HALF_TEXTURE_HEIGHT = TEXTURE_HEIGHT // 2
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# player settings
player_pos = (HALF_WIDTH // 4, HALF_HEIGHT - 50)
player_angle = 0
player_speed = 3

TABEl = {
    "_____": 1,
    "____W": 1,
    "___W_": 1,
    "___WW": -1,
    "__W__": 0,
    "__W_W": 0,
    "__WW_": -1,
    "__WWW": -1,

    "_W___": 1,
    "_W__W": 1,
    "_W_W_": 1,
    "_W_WW": -1,
    "_WW__": -1,
    "_WW_W": 0,
    "_WWW_": 0,
    "_WWWW": 0,

    "W____": -1,
    "W___W": -1,
    "W__W_": -1,
    "W__WW": -1,
    "W_W__": 0,
    "W_W_W": 0,
    "W_WW_": 0,
    "W_WWW": 0,

    "WW___": 0,
    "WW__W": 0,
    "WW_W_": 0,
    "WW_WW": 0,
    "WWW__": 0,
    "WWW_W": 0,
    "WWWW_": 0,
    "WWWWW": 0
}

testDialog = ['тестовый диалог', 'тестовый диалог2', 'тестовый диалог3', 'тестовый диалог4']

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)
DARKBROWN = (97, 61, 25)
DARKORANGE = (255, 140, 0)

PINK = (255, 105, 180)
DARKBLUE = (25, 25, 112)