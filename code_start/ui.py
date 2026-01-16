import os
from settings import *
from sprites import AnimatedSprite

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        
        # hearts
        self.heart_frames = frames['heart']
    
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 5

        # boss healthbar
        self.boss_healthbar_frames = frames['boss_healthbar']
        self.create_boss_healthbar()

    def create_boss_healthbar(self):
        x = WINDOW_WIDTH / 2 - self.boss_healthbar_frames[0].get_width() / 2
        y = 10
        Boss_HealthBar((x,y), self.boss_healthbar_frames, self.sprites)

    def hit_boss(self, amount=1):
        for sprite in self.sprites:
            if isinstance(sprite, Boss_HealthBar):
                sprite.show()
                if amount > 0:
                    sprite.hit(amount)
                return


    def create_hearts(self, num_hearts):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(num_hearts):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)
    
    def update(self, dt):
        self.sprites.update(dt)
        #draw only active sprites
        for sprite in self.sprites:
            if getattr(sprite, 'active', True):
                self.display_surface.blit(sprite.image, sprite.rect)


class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

class Boss_HealthBar(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False
        self.stage = 0
        self.max_stage = len(frames) - 1
        self.image = self.frames[self.stage]

    def show(self):
        self.active = True
        self.image = self.frames[self.stage]

    def hide(self):
        self.active = False

    def hit(self, amount=1):
        self.stage = min(self.stage + amount, self.max_stage)
        self.image = self.frames[self.stage]
        if self.stage >= self.max_stage:
            self.hide()

    def update(self, dt):
        if not self.active:
            return
        self.image = self.frames[self.stage]



