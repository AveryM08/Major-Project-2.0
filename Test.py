from pytmx import load_pygame, TiledMap
import pygame


pygame.init()
S1 = pygame.display.set_mode((800, 600))

tmxdata = load_pygame("data/levels/Quest 1.tmx")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    S1.fill('black')


    for x in range(tmxdata.width):
        for y in range(tmxdata.height):
            image = tmxdata.get_tile_image(x, y, 0)
            S1.blit(image, (x * tmxdata.tilewidth, y * tmxdata.tileheight))


    pygame.display.flip()