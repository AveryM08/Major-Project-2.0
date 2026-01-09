from settings import *
from enemies import *

class Boss_fight:
    def __init__(self, tmx_map, arena_frames, switch_stages):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.switch_stages = switch_stages

        #groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map, arena_frames)

    def setup(self, tmx_map, arena_frames):
        #tiles
        for layer in ['BG', 'Terrain']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)

                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups)