from settings import *
from sprites import AnimatedSprite
from timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        
        # hearts
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 5

        # coins 
        self.coin_frames = frames['coin']
        self.ui_coin = Coin((10, 45), self.coin_frames, self.sprites)
        self.coin_amount = 0
        self.coin_text_surf = None

        # boss healthbar
        self.boss_healthbar_frames = frames['boss_healthbar']
        self.boss_bar = None

    def create_hearts(self, num_hearts):
        for sprite in self.sprites:
            if isinstance(sprite, Heart):
                sprite.kill()
        for heart in range(num_hearts):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)

    def display_coins(self):
        coin_rect = self.ui_coin.rect

        coin_middle_text_surf = self.font.render('x', False, 'white')
        coin_text_surf = self.font.render(str(self.coin_amount), False, 'white')

        # positioning text
        middle_text_rect = coin_middle_text_surf.get_frect(midleft=(coin_rect.right + 10, coin_rect.centery)).move(0, 2)
        text_rect = coin_text_surf.get_frect(midleft=(middle_text_rect.right + 5, middle_text_rect.centery))
    
        full_coin_bg = pygame.FRect(coin_rect.left, coin_rect.top, text_rect.right - coin_rect.left, coin_rect.height).inflate(10, 10)
        self.draw_bar_background(full_coin_bg)

        # drawing text
        self.display_surface.blit(coin_middle_text_surf, middle_text_rect)
        self.display_surface.blit(coin_text_surf, text_rect)

    def show_coins(self, amount):
        self.coin_amount = amount

    def draw_bar_background(self, rect, color=(0, 0, 0, 120)):
        bg_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, color, bg_surf.get_frect(), border_radius=10)
        self.display_surface.blit(bg_surf, rect)

    def create_boss_healthbar(self):
        if self.boss_bar:
            self.boss_bar.kill() 
            self.boss_bar = None

        x = WINDOW_WIDTH / 2 - self.boss_healthbar_frames[0].get_width() / 2
        y = 10
        self.boss_bar = Boss_HealthBar((x,y), self.boss_healthbar_frames, self.sprites)
        self.boss_bar.active = True

    def hide_boss_healthbar(self):
        if self.boss_bar:
            self.boss_bar.active = False

    def hit_boss(self, amount = 1):
        for sprite in self.sprites:
            if isinstance(sprite, Boss_HealthBar):
                # update and show new boss healthbar
                sprite.show()
                if amount > 0:
                    sprite.hit(amount)
                return
        
    def update(self, dt):
        self.sprites.update(dt)
        self.display_coins()

        heart_sprites = [s for s in self.sprites if isinstance(s, Heart)]
        if heart_sprites:
            hearts_rect = pygame.FRect(heart_sprites[0].rect).unionall([s.rect for s in heart_sprites])
            self.draw_bar_background(hearts_rect.inflate(10, 10))
        
        # draw only active sprites
        for sprite in self.sprites:
            if getattr(sprite, 'active', True):
                self.display_surface.blit(sprite.image, sprite.rect)

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

class Coin(AnimatedSprite):
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
        self.image = self.frames[self.stage]