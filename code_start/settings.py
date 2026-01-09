import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6

# layers
Z_LAYERS = {
    'bg': 0,
    'bg tiles': 1,
    'bg details': 2,
    'main': 3
}