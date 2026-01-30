from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Item, ParticleEffectSprite
from player import Player, PropellerPlayer, BossFightPlayer
from groups import AllSprites
from enemies import Diseased_rat, Frog, Boss
from screen_graphics import Graphic, Button

# Player configurations
PLAYER_TYPES = {
    'default': {
        'class': Player,
        'frames': 'default_player',
        'hitbox': 'default'
    },
    'propeller': {
        'class': PropellerPlayer,
        'frames': 'propeller_player',
        'hitbox': 'propeller'
    },
    'boss_fight': {
        'class': BossFightPlayer,
        'frames': 'default_player',
        'hitbox': 'default'
    }
}

class Level:
    def __init__(self, tmx_map, level_frames, screen_frames, audio_files, data, switch_stage):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage
        self.screen_frames = screen_frames['pause_screen']

        self.level_finish_rect = None
        self.boss = None
        
        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        # self.level_unlock = tmx_level_properties['level_unlock']
        if tmx_level_properties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None

        # groups
        self.all_sprites = AllSprites(
            width = tmx_map.width, 
			height = tmx_map.height,
			bg_tile = bg_tile)
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.diseased_rat_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.boss_sprites = pygame.sprite.Group()
        self.setup(tmx_map, level_frames, audio_files)

        # frames
        self.particle_frames = level_frames['particle']

        # audio
        self.coin_sound = audio_files['coin']
        # self.coin_sound.set_volume(0.3) # Adjust volume as needed, 1 = 100% volume
        self.damage_sound = audio_files['damage']
        self.hit_sound = audio_files['hit']

    def setup(self, tmx_map, level_frames, audio_files):
        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semi_collision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        # bg details
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'torch_flame':
                AnimatedSprite((obj.x, obj.y), level_frames['torch_flame'], self.all_sprites, z = Z_LAYERS['bg tiles'])
            elif obj.name == 'torch_base' or obj.name == 'chain':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg tiles'])
            
        # objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == 'Player':
                p_type = obj.type if obj.type else 'default'
                config = PLAYER_TYPES.get(p_type, PLAYER_TYPES['default'])
                player_class = config['class']

                self.player = player_class(
                    pos = (obj.x, obj.y), 
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites,
                    semi_collision_sprites = self.semi_collision_sprites,
                    frames = level_frames[config['frames']],
                    hitbox_config = HITBOX_CONFIGS[config['hitbox']],
                    data = self.data,
                    attack_sound = audio_files['attack'],
                    jump_sound = audio_files['jump'],
                    facing_right = obj.properties.get('facing_right', False),
                    )
            else:
                if obj.name == 'spikes':
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.damage_sprites), upsidedown = obj.properties['upsidedown'],)
            if obj.name == 'portal':
                self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))
            
        # moving objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            frames = level_frames[obj.name]
            groups = (self.all_sprites, self.semi_collision_sprites)
            if obj.name == 'Helicopter':
                if obj.width > obj.height:
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else: # vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed)

        # enemies
        for obj in tmx_map.get_layer_by_name("Enemies"):
            if obj.name == "Boss":
                self.boss = Boss(
                    pos = (obj.x, obj.y),
                    surf = level_frames['boss'],
                    groups = (self.all_sprites, self.collision_sprites, self.boss_sprites),
                    boss_bullets = self.boss_bullets,
                    player = self.player,
                    data = self.data
                )
                
            elif obj.name == 'Diseased_rat':
                all_collideables = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
                Diseased_rat((obj.x, obj.y), level_frames['Diseased_rat'], (self.all_sprites, self.damage_sprites, self.diseased_rat_sprites), all_collideables, obj.properties['speed'])
            
            elif obj.name == 'Frog':
                Frog(
                    pos     = (obj.x, obj.y),
                    frames  = level_frames['Frog'],
                    groups  = (self.all_sprites, self.collision_sprites, self.damage_sprites),
                    reverse = obj.properties['reverse'],
                    player  = self.player
                )

        # items 
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x, obj.y), obj.image, (self.all_sprites, self.item_sprites), self.data)

    def item_collision(self):
        for sprite in self.item_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                sprite.activate()                
                ParticleEffectSprite(sprite.rect.center, self.particle_frames, self.all_sprites)
                self.coin_sound.play()
                sprite.kill()

    def boss_bullet_collision(self):
        for bullet in self.boss_bullets:
            if pygame.sprite.spritecollide(bullet, pygame.sprite.Group(self.player), dokill = False, collided = pygame.sprite.collide_mask):
                bullet.kill()
                ParticleEffectSprite((bullet.rect.center), self.particle_frames, self.all_sprites)
                self.player.take_damage()
                self.damage_sound.play()

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                if hasattr(sprite, 'mask') and sprite.mask:
                    offset = (self.player.hitbox_rect.x - sprite.rect.x, self.player.hitbox_rect.y - sprite.rect.y)

                    if sprite.mask.overlap(pygame.mask.Mask(self.player.hitbox_rect.size, True), offset):
                        self.player.take_damage()
                        self.damage_sound.play()
                
                else:
                    self.player.take_damage()
                    self.damage_sound.play()

    def attack_collision(self):
        if self.player.attacking:
            
            targets = (self.boss_sprites.sprites() + self.diseased_rat_sprites.sprites())
            for target in targets:
                facing_target = ((self.player.rect.centerx < target.rect.centerx and self.player.facing_right) or
                                (self.player.rect.centerx > target.rect.centerx and not self.player.facing_right))
                if target == self.boss:
                    if self.player.attacking and facing_target and pygame.sprite.collide_mask(self.player, target):
                        target.take_damage()
                        self.hit_sound.play()
                        self.data.ui.hit_boss()
                        self.player.attacking = False
                else:
                    if self.player.attacking and facing_target and pygame.sprite.collide_mask(self.player, target):
                        target.speed = 0
                        ParticleEffectSprite((target.rect.center), self.particle_frames, self.all_sprites)
                        self.hit_sound.play()
                        target.kill()

    def check_constraint(self):
		# left right
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width

        # top bottom
        if self.player.hitbox_rect.top <= 0:
            self.player.hitbox_rect.top = 0
        if self.player.hitbox_rect.bottom > self.level_bottom:
            self.player.take_damage()
            self.damage_sound.play()
            self.data.game_state = 'game_over'
            self.switch_stage()

        # death
        if self.data.health <= 0:
            self.data.game_state = 'game_over'
            self.switch_stage()

        # level completion
        if self.level_finish_rect and self.player.hitbox_rect.colliderect(self.level_finish_rect):
            self.switch_stage()
            
        if self.data.boss_health <= 0:
            self.data.game_state = 'game_win'
            self.switch_stage()

    def pause(self):
        overlay = Graphic(self.screen_frames['overlay'], (0, 0), 1)
        resume_button = Button(self.screen_frames['resume_button'], ((WINDOW_WIDTH - (self.screen_frames['resume_button'].get_width()) * 5) // 2, 390), 5)
        restart_button = Button(self.screen_frames['restart_button'], ((WINDOW_WIDTH - (self.screen_frames['restart_button'].get_width()) * 5) // 2, 475), 5)
        quit_button = Button(self.screen_frames['quit_button'], ((WINDOW_WIDTH - (self.screen_frames['quit_button'].get_width()) * 5) // 2, 560), 5)

        overlay.draw(self.display_surface)
        resume_button.draw(self.display_surface)
        if self.data.current_level != 4:
            restart_button.draw(self.display_surface)
        quit_button.draw(self.display_surface)

        if resume_button.is_pressed():
            self.data.game_state = 'running'
        if restart_button.is_pressed():
            self.data.game_state = 'restarting'
            self.switch_stage()
        if quit_button.is_pressed():
            pygame.quit()
            exit()

    def run(self, dt):
        self.display_surface.fill('black')
        
        if self.data.game_state == 'running':
            self.all_sprites.update(dt)
            self.item_collision()
            self.boss_bullet_collision()
            self.attack_collision()
            self.hit_collision()
            self.check_constraint()

        self.all_sprites.draw(self.player.hitbox_rect.center)

        if self.data.game_state == 'paused':
            self.pause()