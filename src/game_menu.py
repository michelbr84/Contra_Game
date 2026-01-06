import pygame.font

class GameMenu:
    def __init__(self, game_settings, screen):
        self.game_settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.title_font = pygame.font.SysFont(None, 80)
        
        self.options = ["Iniciar Jogo", "Sair"]
        self.selected_index = 0
        
        self.build_menu()

    def build_menu(self):
        # Title
        self.title_image = self.title_font.render("CONTRA GAME", True, self.text_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.center = self.screen_rect.center
        self.title_rect.y -= 100
        
    def draw_menu(self):
        # Draw Title
        self.screen.blit(self.title_image, self.title_rect)
        
        # Draw Options
        for index, option in enumerate(self.options):
            color = self.selected_color if index == self.selected_index else self.text_color
            option_image = self.font.render(option, True, color)
            option_rect = option_image.get_rect()
            option_rect.centerx = self.screen_rect.centerx
            option_rect.y = self.title_rect.bottom + 50 + (index * 60)
            self.screen.blit(option_image, option_rect)

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.play_sound('ui_click.mp3')
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.play_sound('ui_click.mp3')
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.select_option()
        return None

    def select_option(self):
        if self.selected_index == 0:
            return 'play'
        elif self.selected_index == 1:
            return 'exit'
    
    def play_sound(self, sound_file):
        try:
             # Assuming play_sound logic is accessible or re-implemented here. 
             # Ideally sharing game_functions logic or accessing mixer directly.
             # For simplicity, using mixer directly as in settings helpers.
             path = self.game_settings.get_sfx_path(sound_file)
             pygame.mixer.Sound(path).play()
        except:
            pass
