import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working on First Screen")

rat = pygame.image.load("graphics/rat.png").convert_alpha()
rat = pygame.transform.scale(rat, (100, 100))

rect_1 = pygame.Rect(200, 100, 150, 100)
rect_2 = rat.get_rect()
rect_2.topleft = (200, 200)

clock = pygame.time.Clock()

running = True
while running:
    
    clock.tick(60)

    screen.fill((225, 225, 225))

    pygame.draw.rect(screen, (225, 0, 225), rect_1)
    pygame.draw.rect(screen, (0, 225, 225), rect_2)

    screen.blit(rat, rect_2)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        rect_2.x -= 5
    if key[pygame.K_d] == True:
        rect_2.x += 5
    if key[pygame.K_w] == True:
        rect_2.y -= 5
    if key[pygame.K_s] == True:
        rect_2.y += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
pygame.quit()