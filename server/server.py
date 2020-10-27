import eventlet
import socketio
from gameSession import GameSession
from sessionTracker import SessionTracker
import threading
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': '../client/index.html'},
    '/game.js': {'content_type': 'text/js', 'filename': '../client/game.js'},
    '/socket-client.js': {'content_type': 'text/js', 'filename': '../client/socket-client.js'},
    '/assets/bg_spooky.png': {'content_type': 'image/png', 'filename': '../assets/bg_spooky.png'},
    '/assets/cobweb.png': {'content_type': 'image/png', 'filename': '../assets/cobweb.png'},
    '/assets/pumpkin.png': {'content_type': 'image/png', 'filename': '../assets/pumpkin.png'},
    '/assets/cake.png': {'content_type': 'image/png', 'filename': '../assets/cake.png'},
    '/assets/cupcakes.png': {'content_type': 'image/png', 'filename': '../assets/cupcakes.png'},
    '/assets/pumpkin_biscuits.png': {'content_type': 'image/png', 'filename': '../assets/pumpkin_biscuits.png'},
    '/assets/pumpkin_cake.png': {'content_type': 'image/png', 'filename': '../assets/pumpkin_cake.png'},
    '/assets/toffee_apples1.png': {'content_type': 'image/png', 'filename': '../assets/toffee_apples1.png'},
    '/assets/ghost.gif': {'content_type': 'image/png', 'filename': '../assets/ghost.gif'},
})

sessionTracker = SessionTracker()

def addNewSnackTimer(gameCode):
    print(f'adding snack for {gameCode}')
    sessionTracker.gameSessions[gameCode].createNewSnack()
    threading.Timer(3, lambda: addNewSnackTimer(gameCode)).start()

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
def startNewGameSession(sid):
    print(f'starting a new game session')
    # create GameSession
    # add new game session to gameSessions dict
    gameCode = sessionTracker.addNewSession()
    # create host player
    newPlayer = sessionTracker.gameSessions[gameCode].registerNewPlayer(sid)
    sio.emit('newGameCode', {'gameCode': gameCode, 'token': newPlayer.token, 'position': newPlayer.position}, room=sid)
    addNewSnackTimer(gameCode)

@sio.event
def registerPlayerToGame(sid, gameCode):
    print(f'registering player with gameCode {gameCode}')
    newPlayer = sessionTracker.gameSessions[gameCode].registerNewPlayer(sid)
    sio.emit('newPlayerToken', {'token': newPlayer.token, 'gameCode': gameCode, 'position': newPlayer.position}, room=sid)
    broadcastNewPlayerJoined(gameCode, newPlayer)

@sio.event
def updatePlayerInfo(sid, playerData):
    sessionTracker.gameSessions[playerData["gameCode"]].registeredPlayers[playerData["playerToken"]].update(playerData)
    player = sessionTracker.gameSessions[playerData["gameCode"]].registeredPlayers[playerData["playerToken"]]
    playerPosition = player.position
    removedSnacks = []
    # check for snack collision
    for snack in dict.values(sessionTracker.gameSessions[playerData["gameCode"]].snacks):
        # position = json.loads(player.position)
        if(abs(snack["x"] - playerPosition["x"]) < 50 and abs(snack["y"] - playerPosition["y"]) < 50):
            removedSnacks.append(snack["token"])

    for token in removedSnacks:
        sessionTracker.gameSessions[playerData["gameCode"]].snackConsumedByPlayer(player.token, snack["token"])
    
    broadcastPlayerInfo(playerData["gameCode"])

def broadcastNewPlayerJoined(gameCode, player):
    for playerBroadcast in dict.values(sessionTracker.gameSessions[gameCode].registeredPlayers):
        sio.emit('broadcastNewPlayerJoined', { "position": player.position, "token": player.token }, room=playerBroadcast.sid)

def broadcastPlayerInfo(gameCode):
    for player in dict.values(sessionTracker.gameSessions[gameCode].registeredPlayers):
        playersData = list(map(lambda player: { "position": player.position, "token": player.token, "score": player.score }, dict.values(sessionTracker.gameSessions[gameCode].registeredPlayers)))
        sio.emit('playersInfoBroadcast', {"playersData": playersData, "snacksData": sessionTracker.gameSessions[gameCode].snacks}, room=player.sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)