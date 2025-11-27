import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working on First Screen")

# surf 1
original_Rat_surf_1 = pygame.image.load("graphics/standing rat-1.png")
original_Rat_surf_1 = pygame.transform.scale(original_Rat_surf_1, (100, 100))

original_Rat_surf_2 = pygame.image.load("graphics/standing rat-2.png")
original_Rat_surf_2 = pygame.transform.scale(original_Rat_surf_2, (100, 100))

Rat_surf = [original_Rat_surf_1, original_Rat_surf_2]
current_Rat_surf = Rat_surf[0]

# surf 2
flipped_Rat_surf_1 = pygame.transform.flip(original_Rat_surf_1, True, False)
flipped_Rat_surf_2 = pygame.transform.flip(original_Rat_surf_2, True, False)
flipped_Rat_surf = [flipped_Rat_surf_1, flipped_Rat_surf_2]

# surf 3
original_WalkingRat_surf_1 = pygame.image.load("graphics/walking rat-1.png")
original_WalkingRat_surf_1 = pygame.transform.scale(original_WalkingRat_surf_1, (100, 100))

original_WalkingRat_surf_2 = pygame.image.load("graphics/walking rat-2.png")
original_WalkingRat_surf_2 = pygame.transform.scale(original_WalkingRat_surf_2, (100, 100))
WalkingRat_surf = [original_WalkingRat_surf_1, original_WalkingRat_surf_2]

# surf 4
flipped_WalkingRat_surf_1 = pygame.transform.flip(original_WalkingRat_surf_1, True, False)
flipped_WalkingRat_surf_2 = pygame.transform.flip(original_WalkingRat_surf_2, True, False)
flipped_WalkingRat_surf = [flipped_WalkingRat_surf_1, flipped_WalkingRat_surf_2]

is_flipped = False
game_active = True
i = 0

Rat_rect = current_Rat_surf.get_rect(center = (300, 200))

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

    is_walking = False

    key = pygame.key.get_pressed()
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        Rat_rect.move_ip(-5, 0)
        is_walking = True

        if is_flipped:
            is_flipped = False
        
        if i < 1:
            current_Rat_surf = WalkingRat_surf[0]
        if i >= 1 and i < 2:
            current_Rat_surf = WalkingRat_surf[1]
        if i == 2:
            i = 0

    if key[pygame.K_d] or key[pygame.K_RIGHT]:
        Rat_rect.move_ip(5, 0)
        is_walking = True
        if not is_flipped:
            is_flipped = True

        if i < 1:
            current_Rat_surf = flipped_WalkingRat_surf[0]
        if i >= 1 and i < 2:
            current_Rat_surf = flipped_WalkingRat_surf[1]
        if i == 2:
            i = 0

    if key[pygame.K_w] or key[pygame.K_UP]:
        Rat_rect.move_ip(0, -5)
    if key[pygame.K_s] or key[pygame.K_DOWN]:
        Rat_rect.move_ip(0, 5)

    if is_walking == False and i < 1:
        if is_flipped:
            current_Rat_surf = flipped_Rat_surf[0]
        else:
            current_Rat_surf = Rat_surf[0]
    if is_walking == False and i >= 1 and i < 2:
        if is_flipped:
            current_Rat_surf = flipped_Rat_surf[1]
        else:
            current_Rat_surf = Rat_surf[1]
    
    if i >= 2:
        i = 0

    i += 0.075

    screen.fill((255, 255, 255))
    screen.blit(current_Rat_surf, Rat_rect)

    pygame.time.Clock().tick(60)
    pygame.display.update()
pygame.quit()