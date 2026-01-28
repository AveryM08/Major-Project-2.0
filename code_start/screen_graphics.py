from settings import *

class Graphic:
    def __init__(self, image, pos, scale = 1):
        self.image = image
        self.scale = scale
        self.scale_graphic()
        self.rect = self.image.get_frect(topleft = pos)

    def scale_graphic(self):
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        new_width = int(original_width * self.scale)
        new_height = int(original_height * self.scale)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Button(Graphic):
    def __init__(self, image, pos, scale = 1):
        super().__init__(image, pos, scale)

        self.pressed = False

    def is_pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed and not self.pressed:
                self.pressed = True
                return True
        if not mouse_pressed:
            self.pressed = False
        return False