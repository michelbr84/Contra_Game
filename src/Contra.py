import pygame
import sys
from pygame.locals import *
from settings import Settings
from game_player import Game_Player 
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from game_boss import Game_Boss
from button import Button

def run_game():
	pygame.init()
	pygame.mixer.init()
	game_settings = Settings()
	bg = pygame.image.load(game_settings.get_image_path("map01.jpeg"))
	pos_x = 0#Movimento do mapa
	
	try:
		pygame.mixer.music.load(game_settings.get_music_path("bgm_stage1.mp3"))
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play(-1)
	except Exception as e:
		print(f"Error loading music: {e}")

	screen = pygame.display.set_mode(
		(game_settings.screen_width,game_settings.screen_height))
	pygame.display.set_caption("Jogo Contra")
	stats = GameStats(game_settings)
	player = Game_Player(game_settings,screen)
	bullets = Group()
	boss = Group()
	enemys = Group()
	win_button = Button(game_settings,screen,"VOCÊ VENCEU")
	gf.create_legion(game_settings,screen,enemys)
	gf.create_boss(game_settings,screen,player,boss)
	clock = pygame.time.Clock()

	while True:
		clock.tick(game_settings.fps)
		pygame.mouse.set_visible(False)
		gf.check_events(game_settings,screen,player,bullets)
		gf.update_player(game_settings,stats,player,enemys)
		gf.update_bullet(game_settings,bullets,screen,enemys,boss)	
		gf.update_enemys(game_settings,enemys)	
		gf.update_boss(game_settings,boss)
		gf.update_screen(game_settings,bg,pos_x,screen,player,bullets,enemys,boss,win_button)
		
		if player.moving_right and player.center > player.screen_rect.centerx and game_settings.boss_appear == False:
			game_settings.screen_rolling = True
			pos_x -= 5#Velocidade de rolagem da tela
		else:
			game_settings.screen_rolling = False
run_game()
