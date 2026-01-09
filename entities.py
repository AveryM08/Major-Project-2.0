import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, *args):
        pass


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 24, 24, (0, 200, 255))
        self.speed = 4

    def update(self, keys, collision_grid=None):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        self.rect.x += dx
        self.rect.y += dy
        # TODO: collision check with collision_grid


class Mob(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, (200, 50, 50))


class Chest(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 24, (150, 75, 0))


class Door(Entity):
    def __init__(self, x, y, w=12, h=32):
        super().__init__(x, y, w, h, (100, 100, 200))

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 24, 24, (0, 200, 255))
        self.speed = 4

    def update(self, keys, collision_grid=None):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Try horizontal move
        self.rect.x += dx
        if self.collides(collision_grid):
            self.rect.x -= dx

        # Try vertical move
        self.rect.y += dy
        if self.collides(collision_grid):
            self.rect.y -= dy

    def collides(self, grid, tile_size=8):
        if grid is None:
            return False
        for point in [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright]:
            gx = point[0] // tile_size
            gy = point[1] // tile_size
            if 0 <= gy < len(grid) and 0 <= gx < len(grid[0]):
                if grid[gy][gx] == 1:
                    return True
        return False