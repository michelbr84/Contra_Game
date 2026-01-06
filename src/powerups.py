import pygame
from pygame.sprite import Sprite
import random

class PowerUp(Sprite):
    def __init__(self, game_settings, screen):
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings
        
        # Create a simple image for the powerup
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0)) # Red box
        
        # Render 'S' on it
        self.font = pygame.font.SysFont(None, 24)
        self.text_img = self.font.render("S", True, (255, 255, 255))
        self.text_rect = self.text_img.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.text_img, self.text_rect)
        
        self.rect = self.image.get_rect()
        
        # Random spawn position coming from right
        self.rect.x = game_settings.screen_width
        self.rect.y = random.randint(100, 400) # Random height
        
        self.x = float(self.rect.x)
        self.speed = 2.0
        self.type = 'S' # Spread Gun

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self):
        self.screen.blit(self.image, self.rect)
