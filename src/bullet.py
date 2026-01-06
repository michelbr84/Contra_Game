import pygame
from pygame.sprite import Sprite 

class Bullet(Sprite):

	def __init__(self,game_settings,screen,player, vy_offset=0):
		super().__init__()
		self.game_settings = game_settings
		self.player = player
		self.screen = screen
		self.image = pygame.image.load(self.game_settings.get_image_path('bullet1.png'))
		self.rect = self.image.get_rect()
		self.rect.left = player.rect.right-20#开始子弹默认往右射击
		if self.player.player_direction == -1:
			self.rect.right = player.rect.left+20
		self.rect.centery = player.rect.centery-15
		if self.player.player_down:
			self.rect.centery = player.rect.centery#调整子弹位置
		if self.player.player_up:
			self.rect.bottom = player.rect.top+20
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		
		# Set velocities
		self.speed_factor = game_settings.bullet_speed_factor
		self.vx = 0
		self.vy = vy_offset
		
		if self.player.player_up:
			self.vy = -self.speed_factor
		else:
			self.vx = self.speed_factor * self.player.player_direction
			
	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.rect.x = self.x
		self.rect.y = self.y


	def blit_bullet(self):
	
		self.screen.blit(self.image,self.rect)

