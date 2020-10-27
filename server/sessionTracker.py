from gameSession import *

class SessionTracker:
    def __init__(self):
        self.gameSessions = {}

    def allGameCodes(self):
        return dict.keys(self.gameSessions)

    def addNewSession(self):
        #call game session class to create game session object
        newSession = GameSession()

        #add to gameSessions dict
        self.gameSessions[newSession.gameCode] = newSession
        return newSession.gameCode




