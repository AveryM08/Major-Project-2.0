from settings import *
from random import choice
from timer import Timer
import math
import random
from math import sin

class Diseased_rat(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites, speed = 200):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.z = Z_LAYERS['main']

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = speed

        self.direction_timer = Timer(250)

    def reverse(self):
        if not self.direction_timer.active:
            self.direction *= -1
            self.direction_timer.activate()

    def update(self, dt):
        self.direction_timer.update()

        # animate
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
        self.mask = pygame.mask.from_surface(self.image)

        # move 
        self.rect.x += self.direction * self.speed * dt

        # reverse direction 
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1,1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1,1))
        wall_rect = pygame.FRect(self.rect.topleft + vector(-1,0), (self.rect.width + 2, 1))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
        floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or \
        wall_rect.collidelist(self.collision_rects) != -1:
            self.direction *= -1

class Frog(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player):
        super().__init__(groups)
        self.tongue_groups = (groups[0], groups[2])
        self.remove(groups[-1]) # remove from damage_sprites group (only the tongue does damage)

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
        self.shoot_timer = Timer(5000)
        self.has_attacked = False
        self.able_to_attack = False
        self.current_tongue = None

    def state_management(self):
        player_pos, frog_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = frog_pos.distance_to(player_pos) < 500
        player_front = frog_pos.x < player_pos.x if self.tongue_direction > 0 else frog_pos.x > player_pos.x

        if player_near and player_front and not self.shoot_timer.active:
            self.able_to_attack = True
            self.state = 'attack'
            self.frame_index = 0
            self.shoot_timer.activate()

    def update(self, dt):
        self.shoot_timer.update()
        self.state_management()
        
        animation = True

        # pausing the animation if tongue is still out
        if self.state == 'attack' and self.current_tongue:
            if self.current_tongue and self.current_tongue.alive():
                animation = False

        # animation
        if animation:
            self.frame_index += ANIMATION_SPEED * dt

        # check if animation is complete
        if self.frame_index >= len(self.frames[self.state]):
            if self.state == 'attack':
                if self.able_to_attack:
                    self.has_attacked = False
                    self.shoot_timer.activate()
                else:
                    self.state = 'idle'
                    self.has_attacked = False
            self.frame_index = 0

        self.image = self.frames[self.state][int(self.frame_index)]

        # attack
        if self.state == 'attack' and int(self.frame_index) == 2 and not self.has_attacked:
            self.has_attacked = True
            mouth_offset_x = 12 * self.tongue_direction
            mouth_offset_y = 2
            mouth_pos = (self.rect.centerx + mouth_offset_x, self.rect.centery + mouth_offset_y)
            max_reach = 272

            self.current_tongue = FrogTongue(
                pos        = mouth_pos, 
                direction  = self.tongue_direction, 
                max_length = max_reach,
                groups     = self.tongue_groups,
                speed = 500
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

        elif self.state == 'retracting':
            self.current_length -= self.speed * 1.5 * dt # retract faster
            if self.current_length <= 0:
                self.kill() # remove tongue sprite when fully retracted

        self.draw_tongue()

    def draw_tongue(self):
        end_x = self.start_pos.x + self.current_length * self.direction

        width = max(abs(end_x - self.start_pos.x), 1)
        height = 4 # tongue thickness

        if self.direction < 0:
            topleft = (end_x, self.start_pos.y - height / 2)
        else:
            topleft = (self.start_pos.x, self.start_pos.y - height /2)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (155, 77, 96), (0, 0, width, height))
        
        self.rect = self.image.get_rect(topleft = topleft)

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, boss_bullets, player, data):
        super().__init__(groups)
        self.original_image = surf
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.z = Z_LAYERS['main']
        
        self.last_shot = pygame.time.get_ticks()
        self.stage_management = {
            0: {'health': 14, 'cooldown': 500},
            1: {'health': 7, 'cooldown': 300},
            2: {'health': 0, 'cooldown': 100}
        }

        self.data = data
        self.player = player
        self.stage = 0
        self.health = self.data.boss_health
        self.all_sprites = groups[0]
        self.boss_bullets = boss_bullets

        self.timers = {
            'hit': Timer(400)
        }
        self.angle_offset = 0 
        self.grid_rotation = 0

    def check_stage(self):
        for stage, data in self.stage_management.items():
            if self.health >= data['health']:
                if self.stage != stage:
                    self.stage = stage      
                break
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def flicker(self):
        self.image = self.original_image

        if self.timers['hit'].active and sin(pygame.time.get_ticks() * 150) >= 0:
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf
    
    def take_damage(self):
        if not self.timers['hit'].active:
            self.data.boss_health -= 1
            self.health = self.data.boss_health
            self.timers['hit'].activate()
            if self.health <= 0:
                self.kill()

    def handle_attack(self):
        now = pygame.time.get_ticks()
        cooldown = self.stage_management[self.stage]['cooldown']
        if now - self.last_shot > cooldown:
            self.last_shot = now
            if self.stage == 0:
                self.pattern_one()
            elif self.stage == 1:
                self.pattern_two()
            elif self.stage == 2:
                self.pattern_three()

    def pattern_one(self):
        self.angle_offset += 10 
        for i in range(4):
            angle_deg = (i * (360 / 4)) + self.angle_offset
            angle_rad = math.radians(angle_deg)
            
            vx = math.cos(angle_rad) * 250
            vy = math.sin(angle_rad) * 250
            
            bullet = BossBullet(self.rect.centerx, self.rect.centery, vx, vy)
            self.boss_bullets.add(bullet)
            self.all_sprites.add(bullet)
    
    def pattern_two(self):
        self.grid_rotation += 10
        base_angles = [0, 90, 180, 270]
        speed = 150
        
        for base_angle in base_angles:
            angle_rad = math.radians(base_angle + self.grid_rotation)
            
            vx = math.cos(angle_rad) * speed
            vy = math.sin(angle_rad) * speed
            
            for offset in [-40, 0, 40]:
                off_x = -math.sin(angle_rad) * offset
                off_y = math.cos(angle_rad) * offset
                
                spawn_x = self.rect.centerx + off_x
                spawn_y = self.rect.centery + off_y
                
                bullet = BossBullet(spawn_x, spawn_y, vx, vy)
                self.boss_bullets.add(bullet)
                self.all_sprites.add(bullet)

    def pattern_three(self):
        for _ in range(1):
            angle = math.radians(random.uniform(-30, 30))
            target_pos = vector(self.player.rect.center)

            base_dir = (target_pos - vector(self.rect.center)).normalize()
            vx = (base_dir.x * math.cos(angle) - base_dir.y * math.sin(angle))
            vy = (base_dir.x * math.sin(angle) + base_dir.y * math.cos(angle))
            
            speed = random.uniform(100, 150)
            
            bullet = BossBullet(self.rect.centerx, self.rect.centery, vx * speed, vy * speed)
            self.boss_bullets.add(bullet)
            self.all_sprites.add(bullet)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.check_stage()
        self.handle_attack()
        self.flicker()

        self.mask = pygame.mask.from_surface(self.image)

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        surf = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(surf, pygame.Color('yellow'), (4, 4), 4)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vector(x, y)
        self.vx = vx
        self.vy = vy
        self.z = Z_LAYERS['main']
        self.lifetime = 0
        self.max_lifetime = 10

    def update(self, dt):
        self.pos.x += self.vx * dt
        self.pos.y += self.vy * dt

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)
        
        self.lifetime += dt
        if self.lifetime > self.max_lifetime:
            self.kill()