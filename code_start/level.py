from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Item
from player import Player
from groups import AllSprites
from enemies import Rat, Frog, Boss

class Level:
    def __init__(self, tmx_map, level_frames, data):
        self.display_surface = pygame.display.get_surface()
        self.data = data

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        #tiles
        for layer in ['BG', 'Terrain', 'Platforms']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semi_collision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        #objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "Player":
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites,
                    semi_collision_sprites = self.semi_collision_sprites,
                    frames = level_frames['player'])
            else:
                if obj.name == 'floor_spikes':
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
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
                else: #vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed)

        #enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'boss':
                Boss(
                    pos    = (obj.x, obj.y),
                    frames = level_frames['boss'],
                    groups = (self.all_sprites, self.collision_sprites, self.boss_bullets),
                    player = self.player,
                )
            elif obj.name == 'rat':
                Rat((obj.x, obj.y), level_frames['rat'], (self.all_sprites, self.damage_sprites, self.rat_sprites), self.collision_sprites)
            elif obj.name == 'Frog':
                Frog(
                    pos     = (obj.x, obj.y),
                    frames  = level_frames['Frog'],
                    groups  = (self.all_sprites, self.collision_sprites),
                    reverse = obj.properties['reverse'],
                    player  = self.player
                )
            else:
                pass

        # items 
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)


    # def hit_collision(self):
    #     for sprite in self.damage_sprites:
    #         if sprite.rect.colliderect(self.player.hitbox_rect):
    #             self.player.take_damage(1)  # temporary damage value and method

    # def attack_collision(self):
    #     for target in self.boss_sprites.sprites(): # + any other attackable sprites
    #         facing_target = (self.player.rect.centerx < target.rect.centerx and not self.player.facing_right) or (self.player.rect.centerx > target.rect.centerx and not self.player.facing_right)
    #         if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
    #             pass

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        # self.boss_bullets.update(dt)
        # self.boss_bullets.draw(self.display_surface)
        
        # hits = pygame.sprite.spritecollide(self.player, self.boss_bullets, dokill=True)
        # for bullet in hits:
        #     ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites)
        #     self.player.take_damage(1)   # temporary damage value and method

        # self.hit_collision()
        # self.attack_collision()

        self.all_sprites.draw(self.player.hitbox_rect.center)