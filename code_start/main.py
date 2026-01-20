from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from data import Data
from ui import UI, Boss_HealthBar
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Rat Adventure")
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.data.start_level(0) 
        
        self.tmx_maps = {
            0: load_pygame(join('..', 'data', 'levels', 'Quest 1.tmx')),
            1: load_pygame(join('..', 'data', 'levels', 'Quest 2.tmx'))
            }
        
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.data, map_index = 0)
        # self.current_stage = Level(self.tmx_maps[1], self.level_frames, self.data, map_index = 1)

    def load_new_map(self, map_index):
        # Logic to clear the old map and load the new one

        self.data.start_level(map_index)

    #animations
    def import_assets(self):
        self.level_frames = {
            'cooking_pot': import_folder('..', 'graphics', 'icons', 'cooking_pot'),
            'default_player': import_sub_folders('..', 'graphics', 'player', 'default'),
            'propeller_player': import_sub_folders('..', 'graphics', 'player', 'propeller'),
            'torch_flame': import_folder('..', 'graphics', 'level', 'torch_flame'),
            'Helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'Wind': import_folder('..', 'graphics', 'effects', 'wind_particle'),
            'Frog': import_sub_folders('..', 'graphics', 'enemies', 'frog'),
            'items': import_sub_folders('..', 'graphics', 'items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
            'boss': import_folder('..', 'graphics', 'enemies', 'boss'),
        }

        self.font = pygame.font.Font(join('..', 'graphics','ui','runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_folder('..', 'graphics', 'ui', 'heart'),
            'coin':import_image('..', 'graphics', 'ui', 'coin'),
            'boss_healthbar': import_folder('..', 'graphics', 'ui', 'boss_healthbar'),
        }
        self.quest_2_frames = {
            'particle': import_sub_folders('..', 'graphics', 'effects', 'particle'),
            'player': import_sub_folders('..', 'graphics', 'player', 'default')
        }

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.current_stage.run(dt)
            self.ui.update(dt)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()