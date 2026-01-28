from settings import *
from level import Level
from screen import Screen
from pytmx.util_pygame import load_pygame
from os.path import join
from data import Data
from ui import UI, Boss_HealthBar
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sewer Savior")
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.data.start_level(1) # This starts at level 0, edit the number while testing to start at different levels

        self.tmx_maps = {
            1: load_pygame(join('..', 'data', 'levels', 'Quest 1 - Copy.tmx')),
            2: load_pygame(join('..', 'data', 'levels', 'Quest 1.tmx')),
            3: load_pygame(join('..', 'data', 'levels', 'Quest 2.tmx')),
            4: load_pygame(join('..', 'data', 'levels', 'Start.tmx')),
            }
        
        # self.current_stage = Screen(self.screen_frames, self.switch_stage)
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.data, self.switch_stage)

    def switch_stage(self):
        self.data.current_level += 1
        if self.data.current_level in self.tmx_maps:
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.data, self.switch_stage)
        else:
            print("You win!")
            # End game screen here instead of print statement
            # self.current_stage = Screen(self.screen_frames, self.switch_stage)

    #animations
    def import_assets(self):
        self.level_frames = {
            'cooking_pot': import_folder('..', 'graphics', 'icons', 'cooking_pot'),
            'default_player': import_sub_folders('..', 'graphics', 'player', 'default'),
            'propeller_player': import_sub_folders('..', 'graphics', 'player', 'propeller'),
            'torch_flame': import_folder('..', 'graphics', 'level', 'torch_flame'),
            'Helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'Wind': import_folder('..', 'graphics', 'effects', 'wind_particle'),
            'Diseased_rat': import_folder('..', 'graphics', 'enemies', 'diseased_rat', 'idle'),
            'Frog': import_sub_folders('..', 'graphics', 'enemies', 'frog'),
            'items': import_sub_folders('..', 'graphics', 'items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
            'boss': import_folder('..', 'graphics', 'enemies', 'boss'),
        }

        self.font = pygame.font.Font(join('..', 'graphics','ui','runescape_uf.ttf'), 35)
        self.ui_frames = {
            'heart': import_folder('..', 'graphics', 'ui', 'heart'),
            'coin':import_folder('..', 'graphics', 'ui', 'coin'),
            'boss_healthbar': import_folder('..', 'graphics', 'ui', 'boss_healthbar'),
        }
        self.quest_2_frames = {
            'particle': import_sub_folders('..', 'graphics', 'effects', 'particle'),
            'player': import_sub_folders('..', 'graphics', 'player', 'default') # unnessecary? idk
        }

        self.screen_frames = {
            'background': import_folder('..', 'graphics', 'background'),
            'game_title': import_image('..', 'graphics', 'game', 'title'),
            'next_button': import_image('..', 'graphics', 'buttons', 'Next Button'),
            'quit_button': import_image('..', 'graphics', 'buttons', 'Quit Button'),
            'start_button': import_image('..', 'graphics', 'buttons', 'Start Button'),
            'back_button': import_image('..', 'graphics', 'buttons', 'Back Button'),
        }

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # self.current_screen.run()
            self.current_stage.run(dt)
            # self.ui.update(dt)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()