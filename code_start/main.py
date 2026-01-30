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
        self.data.start_level(0)

        self.tmx_maps = {
            1: load_pygame(join('..', 'data', 'levels', '1.tmx')),
            2: load_pygame(join('..', 'data', 'levels', '2.tmx')),
            3: load_pygame(join('..', 'data', 'levels', '3.tmx')),
            4: load_pygame(join('..', 'data', 'levels', 'boss_fight.tmx'))
            }
        
        self.current_stage = Screen(self.screen_frames, self.data, self.switch_stage)
        # self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.screen_frames, self.audio_files, self.data, self.switch_stage)
        self.bg_audio.play(-1)

    def switch_stage(self):
        if self.data.game_state == 'game_over' or self.data.game_state == 'game_win':
            self.data.coins = 0  # Reset coins when starting a new game
            self.data.start_level(0)
            self.current_stage = Screen(self.screen_frames, self.data, self.switch_stage)
        
        else:
            self.data.health = 5  # Reset health when starting a new level/game
            if self.data.game_state == 'restarting':
                self.data.coins = 0  # Reset coins when restarting level
                self.data.boss_health = 21 # Reset boss health when restarting level (if applicable)
                self.data.game_state = 'running'
                self.data.start_level(self.data.current_level)
            else: # advance to next level
                self.data.start_level(self.data.current_level + 1)
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.screen_frames, self.audio_files, self.data, self.switch_stage)

    # animations
    def import_assets(self):
        self.level_frames = {
            'default_player': import_sub_folders('..', 'graphics', 'player', 'default'),
            'propeller_player': import_sub_folders('..', 'graphics', 'player', 'propeller'),
            'torch_flame': import_folder('..', 'graphics', 'level', 'torch_flame'),
            'Helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'Wind': import_folder('..', 'graphics', 'effects', 'wind_particle'),
            'Diseased_rat': import_folder('..', 'graphics', 'enemies', 'diseased_rat', 'idle'),
            'Frog': import_sub_folders('..', 'graphics', 'enemies', 'frog'),
            'items': import_sub_folders('..', 'graphics', 'items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
            'boss': import_image('..', 'graphics', 'enemies', 'boss'),
        }
        
        self.screen_frames = {
            'first_screen': {
                'background': import_image('..', 'graphics', 'screen', 'first', 'background'),
                'text': import_image('..', 'graphics', 'screen', 'first', 'text'),
                'start_button': import_image('..', 'graphics', 'screen', 'first', 'button', 'Start'),
                'quit_button': import_image('..', 'graphics', 'screen', 'first', 'button', 'Quit'),
            },

            'pause_screen': {
                'overlay': import_image('..', 'graphics', 'screen', 'pause', 'overlay'),
                'resume_button': import_image('..', 'graphics', 'screen', 'pause', 'button', 'Resume'),
                'restart_button': import_image('..', 'graphics', 'screen', 'pause', 'button', 'Restart'),
                'quit_button': import_image('..', 'graphics', 'screen', 'pause', 'button', 'Quit'),
            },

            'win_screen': {
                'background': import_image('..', 'graphics', 'screen', 'win', 'background'),
                'text': import_image('..', 'graphics', 'screen', 'win', 'text'),
                'quit_button': import_image('..', 'graphics', 'screen', 'win', 'button', 'Quit'),
            },

            'game_over_screen': {
                'background': import_image('..', 'graphics', 'screen', 'game_over', 'background'),
                'text': import_image('..', 'graphics', 'screen', 'game_over', 'text'),
                'restart_button': import_image('..', 'graphics', 'screen', 'game_over', 'button', 'Restart'),
                'quit_button': import_image('..', 'graphics', 'screen', 'game_over', 'button', 'Quit'),
            }
        }

        self.ui_frames = {
            'heart': import_folder('..', 'graphics', 'ui', 'heart'),
            'coin':import_folder('..', 'graphics', 'ui', 'coin'),
            'boss_healthbar': import_folder('..', 'graphics', 'ui', 'boss_healthbar'),
        }

        self.font = pygame.font.Font(join('..', 'graphics','ui','runescape_uf.ttf'), 35)

        self.audio_files = {
            'jump': pygame.mixer.Sound(join('..', 'audio', 'jump.wav')),
            'coin': pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
            'hit': pygame.mixer.Sound(join('..', 'audio', 'hit.wav')),
            'attack': pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
            'damage': pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
        }

        self.bg_audio = pygame.mixer.Sound(join('..', 'audio', 'background.mp3'))
        self.bg_audio.set_volume(0.3)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.data.game_state = 'paused' if self.data.game_state == 'running' else 'running'
            
            if self.data.current_level == 0:
                self.current_stage.run()
            else:
                self.current_stage.run(dt)
            
            if self.data.current_level >= 1 and self.data.game_state == 'running' or self.data.game_state == 'paused':
                self.ui.update(dt)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()