from settings import *
from random import choice
import math

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player):
        super().__init__(groups)
        self.frames, self.frame_index= frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = Z_LAYERS['main']
        #Import graphics in main.py later
        self.old_rect = self.rect.copy()
        self.player = player
        self.health = 1000
        self.stage = 0

        self.shoot_timer = Timer(1000)
        self.has_fired = False
        self.direction = choice((-1,1))

    def stage_management(self):
        if self.health <= 500:
            self.stage = 1
        if self.health <= 250:
            self.stage = 2

class Bullet_1(pygame.sprite.Sprite):
    def __init__(self, player_pos, target_pos, groups, surf, speed):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = player_pos)
        self.pos = pygame.math.Vector2(player_pos)
        self.speed = speed
        self.z = Z_LAYERS['main']
        direction = pygame.math.Vector2(target_pos) - self.pos
        if direction.length() != 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

class Bullet_2(pygame.sprite.Sprite):
    def __init__(self, pos, angle, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.angle = angle
        self.speedy = 5*math.sin(math.radians(self.angle))
        self.speedx = 5*math.cos(math.radians(self.angle))
        self.posx = self.rect.centerx
        self.posy = self.rect.centery
    
        self.z = Z_LAYERS['main']
      

    def update(self, dt):
        self.posx += self.speedx
        self.posy += self.speedy
        self.rect.center = (round(self.posx), round(self.posy))
        if(self.rect.right < 0 or self.rect.left > window_width or self.rect.bottom < 0 or self.rect.top > window_height):
            self.kill()