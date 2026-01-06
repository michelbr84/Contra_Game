import sys
import pygame
from bullet import Bullet
from enemy import Enemy 
from game_boss import Game_Boss
from powerups import PowerUp
import random


def play_sound(game_settings, sound_file):
	try:
		sound = pygame.mixer.Sound(game_settings.get_sfx_path(sound_file))
		sound.play()
	except Exception as e:
		print(f"Error playing sound {sound_file}: {e}")


def check_keydown_events(event,game_settings,screen,player,bullets):
	if event.key == pygame.K_k:#Pular
		player.player_jump = True
		play_sound(game_settings, 'player_jump.mp3')

	if event.key == pygame.K_d:#Direita
		game_settings.bullet_direction = 'right' 
		if player.player_down or player.player_up:
			player.moving_right = False
		else:
			player.moving_right = True
		player.player_direction = 1	

	if event.key == pygame.K_a:#Esquerda
		game_settings.bullet_direction = 'left'
		if player.player_down or player.player_up:
			player.moving_left = False
		else:
			player.moving_left = True
		player.player_direction = -1

	elif event.key == pygame.K_s:#Baixo
		player.player_down = True
		player.player_moving = False
		player.moving_left = False
		player.moving_right = False

	elif event.key == pygame.K_w:#Cima
		player.player_up = True
		player.player_moving = False
		player.moving_left = False
		player.moving_right = False

	elif event.key == pygame.K_j:#Atirar

		if player.bullet_type == 'S':
			# Spread Gun: 3 bullets
			# Center
			bullets.add(Bullet(game_settings,screen,player, vy_offset=0))
			# Up Diagonal
			bullets.add(Bullet(game_settings,screen,player, vy_offset=-3))
			# Down Diagonal
			bullets.add(Bullet(game_settings,screen,player, vy_offset=3))
		else:
			# Normal Gun
			new_bullet = Bullet(game_settings,screen,player)
			bullets.add(new_bullet)
			
		player.player_shooting = True
		play_sound(game_settings, 'player_shoot.mp3')

	elif event.key == pygame.K_p:
		sys.exit()

def check_keyup_events(event,player):
	if event.key == pygame.K_d:#Direita
		player.image = pygame.image.load(player.game_settings.get_image_path('PR/player.png'))
		player.moving_right = False
		player.player_moving = False
	elif event.key == pygame.K_a:#Esquerda
		player.image = pygame.image.load(player.game_settings.get_image_path('PL/player.png'))
		player.player_moving = False
		player.moving_left = False
	elif event.key == pygame.K_s:#Baixo
		player.player_down = False
		if player.player_direction == 1:
			player.image = pygame.image.load(player.game_settings.get_image_path('PR/player.png'))
		if player.player_direction == -1:
			player.image = pygame.image.load(player.game_settings.get_image_path('PL/player.png'))
	elif event.key == pygame.K_w:#Cima
		player.player_up = False
		if player.player_direction == 1:
			player.image = pygame.image.load(player.game_settings.get_image_path('PR/player.png'))
		if player.player_direction == -1:
			player.image = pygame.image.load(player.game_settings.get_image_path('PL/player.png'))
	
def check_events(game_settings,screen,player,bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			player.player_moving = True
			check_keydown_events(event,game_settings,screen,player,bullets)		
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,player)

def update_screen(game_settings,bg,pos_x,screen,player,bullets,enemys,boss,win_button, powerups, sb):
	screen.blit(bg,(pos_x,0))
	for bullet in bullets.sprites():
		bullet.blit_bullet()
	"""if game_settings.boom_end:#Explosão ao atingir o inimigo
		enemys.empty()
		game_settings.boom_end = False"""
	player.blitme()
	if game_settings.boss_appear:
		boss.draw(screen)
	enemys.draw(screen)
	powerups.draw(screen)
	sb.show_score()

	if game_settings.game_win:
		win_button.draw_button()
		play_sound(game_settings, 'level_complete.mp3')
	pygame.display.flip()

def update_bullet(game_settings,bullets,screen,enemys,boss, stats, sb):
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.centerx<0 or bullet.rect.centery<0 or bullet.rect.centerx > game_settings.screen_width:
			bullets.remove(bullet)
	check_bullet_enemy_collisions(game_settings,bullets,screen,enemys, stats, sb)
	check_bullet_boss_collisions(game_settings,bullets,boss, stats, sb)
	

def check_bullet_enemy_collisions(game_settings,bullets,screen,enemys, stats, sb):
	if game_settings.enemy_is_alive:
		collisions = pygame.sprite.groupcollide(bullets,enemys,True,False)
	else:
		collisions = pygame.sprite.groupcollide(bullets,enemys,True,True)
	if collisions != {}:
		game_settings.enemy_is_alive = False
		play_sound(game_settings, 'enemy_hit.mp3')
		stats.score += 50
		sb.prep_score()
		if stats.score > stats.high_score:
			stats.high_score = stats.score
			sb.prep_high_score()
			stats.save_high_score()
	if len(enemys) == 0:
		create_legion(game_settings,screen,enemys)

def check_bullet_boss_collisions(game_settings,bullets,boss, stats, sb):
	if game_settings.boss_alive:
		collisions = pygame.sprite.groupcollide(boss,bullets,False,True)
	else:
		collisions = pygame.sprite.groupcollide(boss,bullets,True,True)

	if collisions != {}:
		game_settings.boss_lift -= 1
	if game_settings.boss_lift == 0:
		game_settings.boss_alive = False
		play_sound(game_settings, 'explosion.mp3')
		stats.score += 500
		sb.prep_score()
		if stats.score > stats.high_score:
			stats.high_score = stats.score
			sb.prep_high_score()
			stats.save_high_score()

def create_legion(game_settings,screen,enemys):
	for enemy_number in range(1):
		game_settings.enemy_is_alive = True
		enemy = Enemy(game_settings,screen)
		enemys.add(enemy)

def update_enemys(game_settings,enemys):
	if game_settings.boss_appear == False:#Verifica se o boss apareceu, se sim, não aparecem minions
		enemys.update()

		for enemy in enemys.copy():
			if enemy.rect.centerx<0:
				enemys.remove(enemy)
			if game_settings.boom_end:#击中敌人爆炸
				enemys.remove(enemy)
				game_settings.boom_end = False
				game_settings.boss_appear = True
				play_sound(game_settings, 'boss_appear.mp3')

def update_powerups(game_settings, powerups, player):
	powerups.update()
	
	# Random spawn
	if len(powerups) < 1 and random.randint(1, 1000) == 1: # 0.1% chance per frame if empty
		powerups.add(PowerUp(game_settings, player.screen))
		
	# Collision with player
	hit_powerup = pygame.sprite.spritecollideany(player, powerups)
	if hit_powerup:
		player.bullet_type = hit_powerup.type
		play_sound(game_settings, 'powerup_pickup.mp3')
		powerups.remove(hit_powerup)

def update_player(game_settings,stats,player,enemys, powerups):
	player.update()
	if pygame.sprite.spritecollideany(player,enemys):
		player_hit(game_settings,stats,player)
	if game_settings.player_die_end == True:
		player.revive_player()
		game_settings.player_die_end = False

def player_hit(game_settings,stats,player):
	stats.players_left -= 1
	game_settings.player_is_alive = False
	play_sound(game_settings, 'player_hit.mp3')
	
def update_boss(game_settings,boss):
	if game_settings.boss_appear:
		boss.update()
	if game_settings.boss_boom_end:
		boss.empty()

def create_boss(game_settings,screen,player,boss):
	bo = Game_Boss(game_settings,screen,player)
	boss.add(bo)