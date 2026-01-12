
from settings import * 
from level import Level
from pytmx import load_pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Major Project 2.0")

        self.tmx_maps = {0: load_pygame("data/levels/Start.tmx")}

        self.current_level = Level(self.tmx_maps[0])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_level.run()

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()

