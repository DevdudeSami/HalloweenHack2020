import random
import string
from player import * 
import threading, time

def generateSnackToken():
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))

class GameSession:
	def __init__(self):
		self.gameCode = GameSession.generateCode() #generate random code
		# while(not checkCode(self.gameCode)):
		# 	self.gameCode = generateCode()

		self.snacks = {}
		self.registeredPlayers = {} # dictionary of player tokens to Player

	@staticmethod
	def generateCode():     
		return ''.join(random.choice(string.ascii_uppercase) for _ in range(4)) #generate random game code code

	def createNewSnack(self):
		snack_images= [
			"cake",
			"cupcakes",
			"pumpkin_biscuits",
			"pumpkin_cake",
			"toffee_apples1"
		]
		snackToken = generateSnackToken()
		self.snacks[snackToken] = {
			"token": snackToken,
			"image": random.choice(snack_images),
			"x": random.randint(0, 2881 // 3),
			"y": random.randint(0, 1620 // 3)
			}

	def snackConsumedByPlayer(self, playerToken, snackToken):
		self.snacks.pop(snackToken, None)
		self.registeredPlayers[playerToken].score += 1

	def registerNewPlayer(self, sid):
		# create new player object
		player = Player(sid)
		# add it to dict with token as key
		self.registeredPlayers[player.token] = player
		return player

#	@staticmethod
#	def checkCode(gameCode):
	#	#check game code not already in use
	#		return gameCode not in SessionTracker.allGameCodes() #TODO: 
           



