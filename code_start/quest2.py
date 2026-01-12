from settings import *
from groups import WorldSprites
from random import randint
from sprites import Sprite
from player import Quest2Player

class Boss_fight:
    def __init__(self, tmx_map, data, frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data

        #groups
        self.all_sprites = WorldSprites(data)
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map, quest_2_frames)

    def setup(self, tmx_map, quest_2_frames):
        #tiles
        for layer in ['BG', 'Terrain']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                if layer == 'BG':
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, Z_LAYERS['bg tiles'])
                if layer == 'Terrain': 
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, Z_LAYERS['main'])

        #objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == 'Player':
                self.player = Quest2Player((obj.x, obj.y), (self.all_sprites,), self.collision_sprites, self.semi_collision_sprites)

    def run(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw((0,0)) #offset at 0,0 for now. Change when map works