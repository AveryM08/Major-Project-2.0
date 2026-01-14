from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from data import Data
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Rat Adventure")
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.data = Data(self.ui)
        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'Quest 1.tmx'))}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)

    def import_assets(self):
        self.level_frames = {
            'cooking_pot': import_folder('..', 'graphics', 'icons', 'cooking_pot'),
            'player': import_sub_folders('..', 'graphics', 'player', 'default'),
            'Helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'Wind': import_folder('..', 'graphics', 'effects', 'wind_particle'),
            'Frog': import_sub_folders('..', 'graphics', 'enemies', 'frog'),
            'items': import_sub_folders('..', 'graphics', 'items'),
        }

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.current_stage.run(dt)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()