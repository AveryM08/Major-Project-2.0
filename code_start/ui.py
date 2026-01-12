from settings import *
from sprites import AnimatedSprite

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 5
        self.boss_healthbar_frames = frames['boss_healthbar']
        self.create_hearts(5)
        self.create_boss_healthbar()

    def create_boss_healthbar(self):
        x = WINDOW_WIDTH / 2 - self.boss_healthbar_frames[0].get_width() / 2
        y = 10
        Boss_HealthBar((x,y), self.boss_healthbar_frames, self.sprites)

    def create_hearts(self, num_hearts):
        for heart in range(num_hearts):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)
    
    def update(self, dt):
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

class Boss_HealthBar(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

