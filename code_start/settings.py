import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 768
TILE_SIZE = 64
ANIMATION_SPEED = 3

# layers
Z_LAYERS = {
    'bg': 0,
    'bg tiles': 1,
    'bg details': 2,
    'main': 3,
    'fg': 4
}

HITBOX_CONFIGS = {
    'default': {
        'idle': (-180, 0), # 10 pxl wide
        'run': (-124, 0), # 24 pxl wide, then -6 on top
        'wall': (-176, 0), # 11 pxl wide
        'attack': (-160, 0) # 
    },
    'propeller': {
        'idle': (-180, -72), # 14 pxl tall
        'run': (-124, -72), # diff height but testing with old
        'wall': (-176, 0),
        'freefall': (-176, -48) # The special freefall box
    }
}