// socket io must be available

let socket

$(document).ready(() => {
	connectToSocket()

	socket.on('newGameCode', data => {
		$("#hostGameCode").html(`Your game code is ${data.gameCode}.`)
		localStorage.setItem("playerToken", data.token)
		localStorage.setItem("gameCode", data.gameCode)
		joinedGame(data)
		startGame()
	})

	// when a player joins a game this is sent back to them
	socket.on('newPlayerToken', data => {
		localStorage.setItem("playerToken", data.token)
		localStorage.setItem("gameCode", data.gameCode)
		joinedGame(data)
		startGame()
	})

	socket.on('playersInfoBroadcast', data => {
		updateGameState(data)
	})

	// socket.on('broadcastNewPlayerJoined', data => {
	// 	newPlayerRegistered(data)
	// })

})

function hostNewGame() {
	socket.emit('startNewGameSession')
}

function connectToSocket() {
	socket = io("http://localhost:5000")
}

function startNewGameSession(gameCode) {
	socket.emit('startNewGameSession', gameCode)
}

function registerUser() {
	let gameCode = $("#gameCodeInput").val()
	socket.emit('registerPlayerToGame', gameCode)
}

