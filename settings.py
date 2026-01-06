class Settings():
	def __init__(self):
		self.screen_width = 1200
		self.screen_height = 750
		self.player_speed = 5
		self.jump_vel = -14.0#Velocidade inicial do pulo, se alterar aqui, deve alterar em game_player também
		self.bullet_speed_factor = 17
		self.enemy_speed_factor = 4#A velocidade de rolagem da tela menos a velocidade do inimigo deve ser 1 (tela é 5, inimigo é 4) para ser suave. Se alterar aqui, deve alterar no update do enemy também
		self.screen_rolling = False
		self.enemy_is_alive = True
		self.boom_end = False
		self.players_limit = 3
		self.player_is_alive = True
		self.player_die_end = False
		self.boss_jump_vel = -12.0
		self.attack_1 = False
		self.attack_2 = False
		self.boss_jump = False
		self.boss_run = False
		self.boss_appear = False
		self.boss_direction = 1#1 é para esquerda, -1 é para direita
		self.boss_lift = 15
		self.boss_alive = True
		self.game_win = False
		self.boss_boom_end = False
		self.fps = 60
