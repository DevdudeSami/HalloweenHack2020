# where to store player information plsssss
# a 
import random
import string

class Player:
	def __init__(self, sid):
		self.token = ''.join(random.choice(string.ascii_lowercase + string.digits ) for _ in range(16))
		self.sid = sid
		self.position = {"x": 0, "y": 0}
		self.score = 0

	def update(self, playerData):
		self.position["x"] = int(playerData["position"]["x"])
		self.position["y"] = int(playerData["position"]["y"])

class Inventory:
	def __init__(self):
		pass
