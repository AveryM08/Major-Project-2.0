from settings import *
from random import choice
from timer import Timer
import math
from data import Data

class Rat(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = Z_LAYERS['main']

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 200

    def update(self, dt):
        # animate
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # move
        self.rect.x += self.direction * self.speed * dt

        # reverse direction
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
           floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0:
            self.direction *= -1

class Frog(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player):
        super().__init__(groups)

        if reverse:
            self.frames = {}
            for key, surfs in frames.items():
                self.frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
            self.tongue_direction = -1
        else:
            self.frames = frames
            self.tongue_direction = 1

        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        self.z = Z_LAYERS['main']
        self.player = player
        self.shoot_timer = Timer(3000)
        self.has_attacked = False

    def state_management(self):
        player_pos, frog_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = frog_pos.distance_to(player_pos) < 500
        player_front = frog_pos.x < player_pos.x if self.tongue_direction > 0 else frog_pos.x > player_pos.x
        # player_level = abs(frog_pos.y - player_pos.y < 30)

        if player_near and player_front and not self.shoot_timer.active:
        # if player_near and player_front and player_level and not self.shoot_timer.active:
            self.state = 'attack'
            self.frame_index = 0
            self.shoot_timer.activate()

    def update(self, dt):
        self.shoot_timer.update()
        self.state_management()

        # animate / shoot tongue
        self.frame_index += ANIMATION_SPEED * dt

        # check if animation is complete
        if self.frame_index >= len(self.frames[self.state]):
            if self.state == 'attack':
                self.state = 'idle'
                self.has_attacked = False
                # remove tongue sprite after attack
            self.frame_index = 0

        self.image = self.frames[self.state][int(self.frame_index)]

        # if self.frame_index >= len(self.frames[self.state]):
        #     self.image = self.frames[self.state][int(self.frame_index)]

        # attack
        if self.state == 'attack' and not self.has_attacked: # later update to have it involve self.frame_index
            # if self.state == 'attack' and int(self.frame_index) == 3 and not self.has_attacked:
            self.has_attacked = True
            mouth_offset_x = 12 * self.tongue_direction
            mouth_offset_y = 2
            mouth_pos = (self.rect.centerx + mouth_offset_x, self.rect.centery + mouth_offset_y)
            max_reach = 272

            self.current_tongue = FrogTongue(
                pos        = mouth_pos, 
                direction  = self.tongue_direction, 
                max_length = max_reach,
                groups     = self.groups(),
                speed = 400
            )

class FrogTongue(pygame.sprite.Sprite):
    def __init__(self, pos, direction, max_length, groups, speed):
        super().__init__(groups)
        self.start_pos = vector(pos)
        self.direction = direction
        self.max_length = max_length
        self.speed = speed

        self.z = Z_LAYERS['main']
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = pos)
        self.old_rect = self.rect.copy()

        self.current_length = 0
        self.state = 'extending'

    def update(self, dt):
        self.old_rect = self.rect.copy()

        if self.state == 'extending':
            self.current_length += self.speed * dt
            if self.current_length >= self.max_length:
                self.current_length = self.max_length
                self.state = 'retracting'

            # needs collision detection logic for walls/platforms

        elif self.state == 'retracting':
            self.current_length -= self.speed * 1.5 * dt # retract faster
            if self.current_length <= 0:
                self.kill() # remove tongue sprite when fully retracted

        self.draw_tongue()

    def draw_tongue(self):
        end_x = self.start_pos.x + self.current_length * self.direction
        end_pos = (end_x, self.start_pos.y)

        width = abs(end_x - self.start_pos.x) or 1
        height = 4 # tongue thickness

        if self.direction < 0:
            topleft = (end_x, self.start_pos.y - height / 2)
        else:
            topleft = (self.start_pos.x, self.start_pos.y - height /2)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 100, 100), (0, 0, width, height))
        self.rect = self.image.get_rect(topleft = topleft)

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player):
        super().__init__(groups)
        self.frames, self.frame_index= frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        
        self.last_shot = pygame.time.get_ticks()
        self.stage_management = {
            0: {'health': 750, 'cooldown': 500},
            1: {'health': 350, 'cooldown': 300},
            2: {'health': 0, 'cooldown': 100}
        }
        self.player = player
        self.health = 1000
        self.stage = 0

        # groups passed in by level: (all_sprites, collision_sprites, boss_bullets)
        #remove bugs
        self.boss_bullets = pygame.sprite.Group()

    def check_stage(self):
        for stage, data in self.stage_management.items():
            if self.health >= data['health']:
                if self.stage != stage:
                    self.stage = stage
                break

    def update(self, dt):
        self.check_stage()
        self.handle_attack()

        #animation
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def handle_attack(self):
        now = pygame.time.get_ticks()
        cooldown = self.stage_management[self.stage]['cooldown']
        if now - self.last_shot > cooldown:
            self.last_shot = now
            if self.stage == 0:
                print("single")
                self.pattern_single()
            elif self.stage == 1:
                self.pattern_spread()
            elif self.stage == 2:
                self.pattern_radial()
    
    def pattern_single(self):
        try:
            target_x, target_y = self.player.hitbox_rect.center
        except Exception:
            target_x, target_y = self.player.rect.center

        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        speed = 400.0 
        vx = (dx / distance) * speed
        vy = (dy / distance) * speed
        bullet = BossBullet(self.rect.centerx, self.rect.centery, vx, vy)
        self.boss_bullets.add(bullet)
        if getattr(self, 'all_sprites', None) is not None:
            self.all_sprites.add(bullet)


    def pattern_spread(self, num_bullets=5):
        start_angle = -60
        end_angle = 60
        angle_increment = (end_angle - start_angle) / (num_bullets - 1)
        for i in range(num_bullets):
            angle = math.radians(start_angle + i * angle_increment)
            vx = math.sin(angle) * 200
            vy = math.cos(angle) * 200
            bullet = BossBullet(self.rect.centerx, self.rect.centery, vx, vy)
            self.boss_bullets.add(bullet)
            if getattr(self, 'all_sprites', None) is not None:
                self.all_sprites.add(bullet)

    def pattern_radial(self, num_bullets=8):
        angle_increment = 360 / num_bullets
        for i in range(num_bullets):
            angle = math.radians(i * angle_increment)
            vx = math.sin(angle) * 200
            vy = math.cos(angle) * 200
            bullet = BossBullet(self.rect.centerx, self.rect.centery, vx, vy)
            self.boss_bullets.add(bullet)
            if getattr(self, 'all_sprites', None) is not None:
                self.all_sprites.add(bullet)

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        surf = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(surf, pygame.Color('yellow'), (4, 4), 4)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.z = Z_LAYERS['main']

    def update(self, dt):
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
        if (self.rect.right < 0 or self.rect.left > WINDOW_WIDTH or
            self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT):
            self.kill()