from settings import *
from sprites import Sprite

class Level:
    def __init__(self, tmx_data):
        self.tmx_data = tmx_data
        self.display_surface = pygame.display.get_surface()

        #groups
        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_data)

    def setup(self, tmx_data):
        for x,y,surf in tmx_data.get_layer_by_name('Terrain').tiles():
            Sprite((x * tile_size, y * tile_size), surf, self.all_sprites)
 

    def run(self):
        self.display_surface.fill('black')

