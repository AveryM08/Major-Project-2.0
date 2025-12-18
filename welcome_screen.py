import pygame

class buttons:
   def __init__(self, image_path, position, scale=1):
       self.image = pygame.image.load(image_path).convert_alpha()
       original_width = self.image.get_width()
       original_height = self.image.get_height()
       new_width = int(original_width * scale)
       new_height = int(original_height * scale)
       self.image = pygame.transform.scale(self.image, (new_width, new_height))
       self.rect = self.image.get_rect(topleft=position)
       self.pressed = False


   def draw(self, screen):
       screen.blit(self.image, self.rect)


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

class Player(pygame.sprite.Sprite):
   def __init__(self, image, username):
       super().__init__()
       self.image = image
       self.username = username
       self.rect = self.image.get_rect()

pygame.init()
window = pygame.display.set_mode((1024, 768))
background = pygame.image.load('graphics/background/Main Menu Background.png').convert()
background = pygame.transform.scale(background, window.get_size())
overlay_w = 800
overlay_h = 400
overlay_color = (0,0,0,180)
overlay_surface = pygame.Surface((overlay_w, overlay_h), pygame.SRCALPHA)
overlay_surface.fill(overlay_color)
username = ""
font = pygame.font.Font(None, 60)
player_selected = False 

def show_error_popup(message):
   font = pygame.font.Font(None, 38)
   error_w, error_h = 500, 200
   error_pos = ((1024 - error_w) // 2, (768 - error_h) // 2)
   back_button = buttons('graphics/buttons/Back Button.png', (error_pos[0] + error_w - 140, error_pos[1] + error_h - 80), 4)

   clock_local = pygame.time.Clock()
   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               exit()

       window.blit(background, (0, 0))
       pygame.draw.rect(window, (0,0,0), (error_pos[0], error_pos[1], error_w, error_h))
       message_surf = font.render(message, True, (255, 255, 255))
       window.blit(message_surf, (error_pos[0] + 80, error_pos[1] + 80))


       back_button.draw(window)
       if back_button.is_pressed():
           return
       pygame.display.flip()
       clock_local.tick(60)

def main():
   global username
   clock = pygame.time.Clock()
   username = ""

   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               exit()

       window.fill((0, 0, 0))
       window.blit(background, (0, 0))
       window.blit(overlay_surface, ((1024 - overlay_w) // 2, (768 - overlay_h) // 2))
       next_button = buttons('graphics/buttons/Next Button.png', (362, 420), 4)
       quit_button = buttons('graphics/buttons/Quit Button.png', (550, 420), 4)
       next_button.draw(window)
       quit_button.draw(window)

       if next_button.is_pressed():
           progress()
       if quit_button.is_pressed():
           pygame.quit()
           exit()

       pygame.display.flip()
       clock.tick(60)

def progress():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        window.blit(overlay_surface, ((1024 - overlay_w) // 2, (768 - overlay_h) // 2))
        text_surf = font.render("Select Your Game", True, (255, 255, 255))
        window.blit(text_surf, ((1024 - text_surf.get_width()) // 2, 220))
        game1_button = buttons('graphics/buttons/Game 1 Button.png', ((1024 - 700) // 2, 260), 4)
        game1_button.draw(window)
        game2_button = buttons('graphics/buttons/Game 2 Button.png', ((1024 - 700) // 2, 360), 4)
        game2_button.draw(window)
        game3_button = buttons('graphics/buttons/Game 3 Button.png', ((1024 - 700) // 2, 460), 4)
        game3_button.draw(window)
        back_button = buttons('graphics/buttons/Back Button.png', (775, 510), 4)
        back_button.draw(window)
        if back_button.is_pressed():
            main()
        if game1_button.is_pressed():
            start_username_input()
        if game2_button.is_pressed():
            start_username_input()
        if game3_button.is_pressed():
            start_username_input()
        pygame.display.flip()
        clock.tick(60)

def start_username_input():
    clock = pygame.time.Clock()
    global username
    text_input_box = pygame.Rect(420, 350, 450, 45)
    text_box_active = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
               if text_input_box.collidepoint(event.pos):
                   text_box_active = not text_box_active
               else:
                   text_box_active = False
            if event.type == pygame.KEYDOWN and text_box_active:
               if event.key == pygame.K_BACKSPACE:
                   username = username[:-1]
               else:
                   username += event.unicode
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        window.blit(overlay_surface, ((1024 - overlay_w) // 2, (768 - overlay_h) // 2))

        text_surf = font.render("Username:", True, (255, 255, 255))
        window.blit(text_surf, ((300) // 2, 350))
        pygame.draw.rect(window, (255, 255, 255), text_input_box, 2)
        text_surf = font.render(username, True,(255, 255, 255))
        window.blit(text_surf, (text_input_box.x, text_input_box.y))
        next_button = buttons('graphics/buttons/Next Button.png', (775, 510), 4)
        next_button.draw(window)
        back_button = buttons('graphics/buttons/Back Button.png', (640, 510), 4)
        back_button.draw(window)
        if back_button.is_pressed():
            progress()
        if next_button.is_pressed():
            if username.strip() == "":
                show_error_popup("Username cannot be empty!")
            else:
                choose_rat()
        pygame.display.flip()
        clock.tick(60)

def choose_rat():
    clock = pygame.time.Clock()
    global username, player_selected
    player_selected = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        window.blit(overlay_surface, ((1024 - overlay_w) // 2, (768 - overlay_h) // 2))

        text_surf = font.render("Choose Your Rat:", True, (255, 255, 255))
        window.blit(text_surf, ((1024 - text_surf.get_width()) // 2, 250))
        santa_rat_button = buttons('graphics/buttons/Standing Santa Rat 1.png', (250, 300), 8)
        santa_rat_button.draw(window)
        default_rat_button = buttons('graphics/buttons/Standing Rat 1.png', (550, 300), 8)
        default_rat_button.draw(window)
        back_button = buttons('graphics/buttons/Back Button.png', (640, 510), 4)
        back_button.draw(window)

        if back_button.is_pressed():
            start_username_input()
        if santa_rat_button.is_pressed():
            santa_rat_image = pygame.image.load('graphics/buttons/Standing Santa Rat 1.png').convert_alpha()
            player = Player(santa_rat_image, username)
            player_selected = True
            print("Santa Rat Selected")
        if default_rat_button.is_pressed():
            default_rat_image = pygame.image.load('graphics/buttons/Standing Rat 1.png').convert_alpha()
            player = Player(default_rat_image, username)
            player_selected = True
            print("Default Rat Selected")
        
        pygame.display.flip()
        clock.tick(60)


main()
