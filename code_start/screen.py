from settings import *
from screen_graphics import Graphic, Button

class Screen:
    def __init__(self, screen_frames):
        self.display_surface = pygame.display.get_surface()
        self.background = screen_frames['background'][0]
        self.background = pygame.transform.scale(self.background, self.display_surface.get_size())
        self.overlay_w = 800
        self.overlay_h = 400
        self.overlay_color = (0,0,0,180)
        self.overlay_surface = pygame.Surface((self.overlay_w, self.overlay_h), pygame.SRCALPHA)
        self.overlay_surface.fill(self.overlay_color)
        self.font = pygame.font.Font(None, 60)
        self.screen_frames = screen_frames


    def first_screen(self, screen_frames):
        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.overlay_surface, ((MENU_WIDTH - self.overlay_w) // 2, (MENU_HEIGHT - self.overlay_h) // 2))

        game_title = Graphic(screen_frames['game_title'], ((MENU_WIDTH - (screen_frames['game_title'].get_width()) * 0.25) // 2, 250), 0.25)
        next_button = Button(screen_frames['next_button'], (362, 420), 4)
        quit_button = Button(screen_frames['quit_button'], (550, 420), 4)

        game_title.draw(self.display_surface)
        next_button.draw(self.display_surface)
        quit_button.draw(self.display_surface)

        if next_button.is_pressed():
            # progress()
            print("Next Button Pressed")
        if quit_button.is_pressed():
            pygame.quit()
            exit()

    
    def run(self):
        self.first_screen(self.screen_frames)