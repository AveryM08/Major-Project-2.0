import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working on First Screen")

class image:
    def __init__(self, path, scale):
        self.original_surf = pygame.image.load(path)
        self.original_surf = pygame.transform.scale(self.original_surf, scale)
        self.flipped_surf = pygame.transform.flip(self.original_surf, True, False)

# Default rat surfs
DefaultStandingRat_1 = image("graphics/default/standing rat-1.png", (100, 100))
DefaultStandingRat_2 = image("graphics/default/standing rat-2.png", (100, 100))
DefaultWalkingRat_1 = image("graphics/default/walking rat-1.png", (100, 100))
DefaultWalkingRat_2 = image("graphics/default/walking rat-2.png", (100, 100))

# Chef rat surfs
ChefStandingRat_1 = image("graphics/chef/standing chef rat-1.png", (100, 100))
ChefStandingRat_2 = image("graphics/chef/standing chef rat-2.png", (100, 100))
ChefWalkingRat_1 = image("graphics/chef/walking chef rat-1.png", (100, 100))
ChefWalkingRat_2 = image("graphics/chef/walking chef rat-2.png", (100, 100))

# Santa rat surfs
SantaStandingRat_1 = image("graphics/santa/standing santa rat-1.png", (100, 100))
SantaStandingRat_2 = image("graphics/santa/standing santa rat-2.png", (100, 100))
SantaWalkingRat_1 = image("graphics/santa/walking santa rat-1.png", (100, 100))
SantaWalkingRat_2 = image("graphics/santa/walking santa rat-2.png", (100, 100))

i = 0

default_sprites = {
    "standing": [DefaultStandingRat_1.original_surf, DefaultStandingRat_2.original_surf],
    "standing_flipped": [DefaultStandingRat_1.flipped_surf, DefaultStandingRat_2.flipped_surf],
    "walking": [DefaultWalkingRat_1.original_surf, DefaultWalkingRat_2.original_surf],
    "walking_flipped": [DefaultWalkingRat_1.flipped_surf, DefaultWalkingRat_2.flipped_surf]
}

chef_sprites = {
    "standing": [ChefStandingRat_1.original_surf, ChefStandingRat_2.original_surf],
    "standing_flipped": [ChefStandingRat_1.flipped_surf, ChefStandingRat_2.flipped_surf],
    "walking": [ChefWalkingRat_1.original_surf, ChefWalkingRat_2.original_surf],
    "walking_flipped": [ChefWalkingRat_1.flipped_surf, ChefWalkingRat_2.flipped_surf]
}

santa_sprites = {
    "standing": [SantaStandingRat_1.original_surf, SantaStandingRat_2.original_surf],
    "standing_flipped": [SantaStandingRat_1.flipped_surf, SantaStandingRat_2.flipped_surf],
    "walking": [SantaWalkingRat_1.original_surf, SantaWalkingRat_2.original_surf],
    "walking_flipped": [SantaWalkingRat_1.flipped_surf, SantaWalkingRat_2.flipped_surf]
}

sprites = {
    "default": default_sprites,
    "chef": chef_sprites,
    "santa": santa_sprites
}

class Player(pygame.sprite.Sprite):
    def __init__(self, sprites, selected_sprite_set, spawning_location):
        super().__init__()
        self.sprites = sprites
        self.selected_sprite_set = selected_sprite_set

        self.image = self.sprites[selected_sprite_set]["standing"][0]
        self.rect = self.image.get_rect(center = spawning_location)

        self.is_flipped = False
        self.is_walking = False

        self.pos = pygame.math.Vector2(spawning_location)
        self.vel = pygame.math.Vector2(0, 0)
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = True

    def apply_gravity(self):
        self.vel.y += self.gravity
        self.pos.y += self.vel.y
        self.rect.center = self.pos
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True
            self.vel.y = 0
            self.pos.y = self.rect.centery
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.vel.y = self.jump_strength
            self.on_ground = False

    def move_left(self, i):
        self.pos.x -= 5
        self.rect.center = self.pos

        self.is_walking = True

        if self.is_flipped:
            self.is_flipped = False
        
        if i < 1:
            self.image = self.sprites[self.selected_sprite_set]["walking"][0]
        if i >= 1 and i < 2:
            self.image = self.sprites[self.selected_sprite_set]["walking"][1]

    def move_right(self, i):
        self.pos.x += 5
        self.rect.center = self.pos

        self.is_walking = True

        if not self.is_flipped:
            self.is_flipped = True

        if i < 1:
            self.image = self.sprites[self.selected_sprite_set]["walking_flipped"][0]
        if i >= 1 and i < 2:
            self.image = self.sprites[self.selected_sprite_set]["walking_flipped"][1]
    
    def move_up(self):
        self.rect.move_ip(0, -5)
    
    def move_down(self):
        self.rect.move_ip(0, 5)
    
    def update_stationary(self, i):
        if self.is_walking == False and i < 1:
            if self.is_flipped:
                self.image = self.sprites[self.selected_sprite_set]["standing_flipped"][0]
            else:
                self.image = self.sprites[self.selected_sprite_set]["standing"][0]
        if self.is_walking == False and i >= 1 and i < 2:
            if self.is_flipped:
                self.image = self.sprites[self.selected_sprite_set]["standing_flipped"][1]
            else:
                self.image = self.sprites[self.selected_sprite_set]["standing"][1]

rat = Player(sprites, "santa", (300, 200))
game_active = True

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

    rat.is_walking = False

    key = pygame.key.get_pressed()
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        rat.move_left(i)

    if key[pygame.K_d] or key[pygame.K_RIGHT]:
        rat.move_right(i)

    if key[pygame.K_w] or key[pygame.K_UP]:
        rat.move_up()

    if key[pygame.K_s] or key[pygame.K_DOWN]:
        rat.move_down()

    if key[pygame.K_SPACE]:
        rat.jump()
    
    rat.apply_gravity()
    rat.update_stationary(i)

    if i >= 2:
        i = 0

    i += 0.075

    screen.fill((255, 255, 255))
    screen.blit(rat.image, rat.rect)

    pygame.time.Clock().tick(60)
    pygame.display.update()
pygame.quit()