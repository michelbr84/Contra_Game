import os

class GameStats():
	def __init__(self,game_settings):
		self.game_settings = game_settings
		self.reset_stats()
		self.game_active = False
		self.high_score = 0
		self.load_high_score()

	def reset_stats(self):
		self.players_left = self.game_settings.players_limit
		self.score = 0
		
	def load_high_score(self):
		try:
			path = os.path.join(self.game_settings.base_dir, 'highscore.txt')
			with open(path, 'r') as f:
				self.high_score = int(f.read())
		except:
			self.high_score = 0
			
	def save_high_score(self):
		path = os.path.join(self.game_settings.base_dir, 'highscore.txt')
		with open(path, 'w') as f:
			f.write(str(self.high_score))
