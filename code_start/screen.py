from settings import *
from screen_graphics import Graphic, Button

class Screen:
    def __init__(self, screen_frames, data, switch_stage):
        self.display_surface = pygame.display.get_surface()
        self.screen_frames = screen_frames
        self.data = data
        self.switch_stage = switch_stage

        self.overlay_w = 800
        self.overlay_h = 400
        self.overlay_color = (0,0,0,180)
        self.overlay_surface = pygame.Surface((self.overlay_w, self.overlay_h), pygame.SRCALPHA)
        self.overlay_surface.fill(self.overlay_color)

    def first_screen(self, screen_frames):
        self.display_surface.fill((0, 0, 0))
        background = Graphic(screen_frames['background'], (0,0), 1)
        game_title = Graphic(screen_frames['text'], ((WINDOW_WIDTH - (screen_frames['text'].get_width()) * 0.4) // 2, 250), 0.4)
        start_button = Button(screen_frames['start_button'], (362, 485), 4)
        quit_button = Button(screen_frames['quit_button'], (550, 485), 4)

        background.draw(self.display_surface)
        self.display_surface.blit(self.overlay_surface, ((WINDOW_WIDTH - self.overlay_w) // 2, (WINDOW_HEIGHT - self.overlay_h) // 2))
        game_title.draw(self.display_surface)
        start_button.draw(self.display_surface)
        quit_button.draw(self.display_surface)

        if start_button.is_pressed():
            self.switch_stage()
        if quit_button.is_pressed():
            pygame.quit()
            exit()

    def game_over_screen(self, screen_frames):
        self.display_surface.fill((0, 0, 0))
        background = Graphic(screen_frames['background'], (0,0), 1)
        game_over_text = Graphic(screen_frames['text'], ((WINDOW_WIDTH - (screen_frames['text'].get_width()) * 0.3) // 2, 250), 0.3)
        restart_button = Button(screen_frames['restart_button'], (362, 485), 4)
        quit_button = Button(screen_frames['quit_button'], (550, 485), 4)

        background.draw(self.display_surface)
        self.display_surface.blit(self.overlay_surface, ((WINDOW_WIDTH - self.overlay_w) // 2, (WINDOW_HEIGHT - self.overlay_h) // 2))
        game_over_text.draw(self.display_surface)
        restart_button.draw(self.display_surface)
        quit_button.draw(self.display_surface)
        
        if restart_button.is_pressed():
            self.data.game_state = 'running'
            self.switch_stage()
        if quit_button.is_pressed():
            pygame.quit()
            exit()

    def win_screen(self, screen_frames):
        self.display_surface.fill((0, 0, 0))
        background = Graphic(screen_frames['background'], (0,0), 1)
        win_text = Graphic(screen_frames['text'], ((WINDOW_WIDTH - (screen_frames['text'].get_width()) * 0.5) // 2, 275), 0.5)
        quit_button = Button(screen_frames['quit_button'], ((WINDOW_WIDTH - (screen_frames['quit_button'].get_width()) * 6)//2, 435), 6)

        background.draw(self.display_surface)
        self.display_surface.blit(self.overlay_surface, ((WINDOW_WIDTH - self.overlay_w) // 2, (WINDOW_HEIGHT - self.overlay_h) // 2))
        win_text.draw(self.display_surface)
        quit_button.draw(self.display_surface)
        
        if quit_button.is_pressed():
            pygame.quit()
            exit()

    
    def run(self):
        if self.data.game_state == 'game_over':
            self.game_over_screen(self.screen_frames['game_over_screen'])
        elif self.data.game_state == 'running':
            self.first_screen(self.screen_frames['first_screen'])
        elif self.data.game_state == 'game_win':
            self.win_screen(self.screen_frames['win_screen'])