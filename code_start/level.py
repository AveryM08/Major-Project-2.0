from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Item, ParticleEffectSprite
from player import Player, PropellerPlayer, Quest2Player
from groups import AllSprites
from enemies import Rat, Frog, Boss

class Level:
    def __init__(self, tmx_map, level_frames, data, map_index = None):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.map_index = map_index
        
        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        self.level_unlock = tmx_level_properties['level_unlock']
        if tmx_level_properties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None

        # groups
        self.all_sprites = AllSprites(
            width = tmx_map.width, 
			height = tmx_map.height,
			bg_tile = bg_tile, 
			top_limit = tmx_level_properties['top_limit'],)
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.rat_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.boss_sprites = pygame.sprite.Group()
        self.setup(tmx_map, level_frames, self.map_index)

        # frames
        self.particle_frames = level_frames['particle']

    def setup(self, tmx_map, level_frames, map_index):
        # tiles
        for layer in ['BG', 'Terrain', 'Platforms']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semi_collision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        # bg details
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'torch_flame':
                AnimatedSprite((obj.x, obj.y), level_frames['torch_flame'], self.all_sprites, z = Z_LAYERS['bg tiles'])
            elif obj.name == 'torch_base':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg tiles'])
            
        # objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == 'Player':
                if map_index == 0:
                    self.player = PropellerPlayer(
                        pos = (obj.x, obj.y), 
                        groups = self.all_sprites, 
                        collision_sprites = self.collision_sprites,
                        semi_collision_sprites = self.semi_collision_sprites,
                        frames = level_frames['propeller_player'],
                        hitbox_config = HITBOX_CONFIGS['propeller'],
                        data = self.data,
                        facing_right = obj.properties['facing_right'])
                elif map_index == 1:
                    self.player = Quest2Player(
                        pos = (obj.x, obj.y),
                        groups = (self.all_sprites,),
                        collision_sprites = self.collision_sprites,
                        semi_collision_sprites = self.semi_collision_sprites,
                        frames = level_frames['default_player'],
                        hitbox_config = HITBOX_CONFIGS['default'],
                        data = self.data,)
                else:
                    self.player = Player(
                        pos = (obj.x, obj.y), 
                        groups = self.all_sprites, 
                        collision_sprites = self.collision_sprites,
                        semi_collision_sprites = self.semi_collision_sprites,
                        frames = level_frames['default_player'],
                        hitbox_config = HITBOX_CONFIGS['default'],
                        data = self.data,
                        facing_right = obj.properties['facing_right'])
            else:
                if obj.name == 'spikes':
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.damage_sprites), upsidedown = obj.properties['upsidedown'],)
                # else:
                #     frames = level_frames[obj.name]
                #     AnimatedSprite((obj.x, obj.y), frames, self.all_sprites)

        # moving objects
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            frames = level_frames[obj.name]
            groups = (self.all_sprites, self.semi_collision_sprites) # if obj.properties['Platform'] else (self.all_sprites, self.damage_sprites)
            
            if obj.name == "Wind":
                pass
            elif obj.name == 'Helicopter':
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
                print("Creating boss at:", (obj.x, obj.y))
                self.boss = Boss(
                    pos = (obj.x, obj.y),
                    frames = level_frames['boss'],
                    groups = (self.all_sprites, self.collision_sprites, self.boss_bullets, self.boss_sprites),
                    player = self.player,
                    data = self.data
                )
                
            elif obj.name == 'rat':
                Rat((obj.x, obj.y), level_frames['rat'], (self.all_sprites, self.damage_sprites, self.rat_sprites), self.collision_sprites)
            elif obj.name == 'Frog':
                Frog(
                    pos     = (obj.x, obj.y),
                    frames  = level_frames['Frog'],
                    groups  = (self.all_sprites, self.collision_sprites, self.damage_sprites),
                    reverse = obj.properties['reverse'],
                    player  = self.player
                )
            else:
                pass

        # items 
        for obj in tmx_map.get_layer_by_name('Items'):
            # Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)
            Item(obj.name, (obj.x, obj.y), obj.image, (self.all_sprites, self.item_sprites), data = self.data)

    def item_collision(self):
        for sprite in self.item_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                sprite.activate()                
                ParticleEffectSprite(sprite.rect.center, self.particle_frames, self.all_sprites)
                
                sprite.kill()

    def boss_bullet_collision(self):
        for bullet in self.boss_bullets:
            if pygame.sprite.spritecollide(bullet, pygame.sprite.Group(self.player), dokill = False, collided = pygame.sprite.collide_mask):
                bullet.kill()
                ParticleEffectSprite((bullet.rect.center), self.particle_frames, self.all_sprites)
                self.player.take_damage()

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                self.player.take_damage()

    def attack_collision(self):
        for target in self.boss_sprites.sprites(): # + any other attackable sprites
            facing_target = ((self.player.rect.centerx < target.rect.centerx and self.player.facing_right) or
                             (self.player.rect.centerx > target.rect.centerx and not self.player.facing_right))
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.take_damage()
                self.data.ui.hit_boss()
                self.player.attacking = False

    def check_constraint(self):
		# left right
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width

        # # bottom border 
        # if self.player.hitbox_rect.bottom > self.level_bottom:
        #     self.switch_stage('overworld', -1)

    def run(self, dt):
        self.display_surface.fill('black')

        self.all_sprites.update(dt)
        self.item_collision()
        self.boss_bullet_collision()
        self.hit_collision()
        self.attack_collision()
        self.check_constraint()

        self.all_sprites.draw(self.player.hitbox_rect.center)