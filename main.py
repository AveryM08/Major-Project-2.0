import pygame, sys
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
sys.exit()