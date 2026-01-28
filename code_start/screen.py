from settings import *
from screen_graphics import Graphic, Button

class Screen:
    def __init__(self, screen_frames, data, switch_stage):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage

        self.overlay_w = 800
        self.overlay_h = 400
        self.overlay_color = (0,0,0,180)
        self.overlay_surface = pygame.Surface((self.overlay_w, self.overlay_h), pygame.SRCALPHA)
        self.overlay_surface.fill(self.overlay_color)
        self.font = pygame.font.Font(None, 60)
        self.screen_frames = screen_frames


    def first_screen(self, screen_frames):
        self.display_surface.fill((0, 0, 0))
        background = screen_frames['first_screen']
        background = pygame.transform.scale(background, self.display_surface.get_size())

        self.display_surface.blit(background, (0, 0))
        self.display_surface.blit(self.overlay_surface, ((WINDOW_WIDTH - self.overlay_w) // 2, (WINDOW_HEIGHT - self.overlay_h) // 2))

        game_title = Graphic(screen_frames['game_title'], ((WINDOW_WIDTH - (screen_frames['game_title'].get_width()) * 0.4) // 2, 250), 0.4)
        next_button = Button(screen_frames['next_button'], (362, 475), 4)
        quit_button = Button(screen_frames['quit_button'], (550, 475), 4)

        game_title.draw(self.display_surface)
        next_button.draw(self.display_surface)
        quit_button.draw(self.display_surface)

        if next_button.is_pressed():
            self.switch_stage()
        if quit_button.is_pressed():
            pygame.quit()
            exit()

    def end_screen(self, screen_frames):
        self.display_surface.fill((0, 0, 0))
        background = screen_frames['end_screen']
        background = pygame.transform.scale(background, self.display_surface.get_size())

        self.display_surface.blit(background, (0, 0))
        self.display_surface.blit(self.overlay_surface, ((WINDOW_WIDTH - self.overlay_w) // 2, (WINDOW_HEIGHT - self.overlay_h) // 2))

        win_text = Graphic(screen_frames['win_text'], ((WINDOW_WIDTH - (screen_frames['win_text'].get_width()) * 0.4) // 2, 250), 0.4)
        quit_button = Button(screen_frames['quit_button'], ((WINDOW_WIDTH - (screen_frames['quit_button'].get_width()))//2, 475), 8)

        win_text.draw(self.display_surface)
        quit_button.draw(self.display_surface)
        
        if quit_button.is_pressed():
            pygame.quit()
            exit()

        # self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        # self.background.fill(self.overlay_color)
        # self.display_surface.blit(self.background, (0, 0))

    
    def run(self, dt):
        if self.data.current_level == 0:
            self.first_screen(self.screen_frames)
        else:
            self.end_screen(self.screen_frames)