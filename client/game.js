function startGame() {
	var config = {
		type: Phaser.AUTO,
		width: 2880/3,
		height: 1620/3,
		physics: {
				default: 'arcade',
				arcade: {
						gravity: { y: 200 }
				}
		},
		scene: {
				preload: preload,
				create: create,
				update: update
		}
	};

	var game = new Phaser.Game(config);

	setInterval(updateServer, 25)
}

let player;
let playMoveSpeed = 5;

let gameState = {
	playerCount: 0,
	playerData: {
		// <tokenID>: {
		// 	image:
		// 	...
		// }
	},
	snacksData: {

	}
}

// receives game state updates from the server
async function updateGameState(data) {
	for(let playerData of data.playersData) {
		// if player is not here, add it
		if(!Object.keys(gameState.playerData).includes(playerData.token)) {
			addingNewImageForPlayer = playerData
			// wait for the image to be added
			while(addingNewImageForPlayer != undefined) {
				await new Promise(r => setTimeout(r, 100)); // sleep for a short amount	
			}
		}

		if(playerData.token != localStorage.getItem("playerToken")) {
			gameState.playerData[playerData.token].image.x = playerData.position.x
			gameState.playerData[playerData.token].image.y = playerData.position.y
		} else {
			$("#score").html(playerData.score)
		}
	}

	for(let snack of Object.keys(data.snacksData)) {
		if(!Object.keys(gameState.snacksData).includes(snack.token)) {
			addingNewImageForSnack = data.snacksData[snack]
			// wait for the image to be added
			while(addingNewImageForSnack != undefined) {
				await new Promise(r => setTimeout(r, 100)); // sleep for a short amount	
			}
		}
	}

	// remove deleted snacks
	for(let exisitingSnack of Object.keys(gameState.snacksData)) {
		if(!Object.keys(data.snacksData).includes(exisitingSnack)) {
			// console.log(gameState.snacksData)
			gameState.snacksData[exisitingSnack].image.destroy(true)
			delete gameState.snacksData[exisitingSnack]
		}
	}
}

let addingNewImageForSnack

let addingNewImageForPlayer
function newPlayerRegistered(playerInfo) {
	gameState.playerCount += 1
	addingNewImageForPlayer = playerInfo
}

function joinedGame(playerInfo) {
	// load all previous players
	addingNewImageForPlayer = playerInfo
}

function preload () {
	this.load.setBaseURL('http://localhost:5000/assets');

	this.load.image('player', 'pumpkin.png')
	this.load.image('cobweb', 'cobweb.png');
	this.load.image('pumpkin', 'pumpkin.png');
	this.load.image('bg_spooky', 'bg_spooky.png');
	this.load.image('cake', 'cake.png')
	this.load.image('pumpkin_biscuits', 'pumpkin_biscuits.png');
	this.load.image('pumpkin_cake', 'pumpkin_cake.png');
	this.load.image('toffee_apples1', 'toffee_apples1.png');
	this.load.image('cupcakes', 'cupcakes.png');
	this.load.image('ghost', 'ghost.gif');

	this.load.audio('music', 'tubebackr-space-race.mp3');
}

function create () {
	this.add.image(2880/6, 1620/6, 'bg_spooky');

	// music = this.add.audio('music');
	// music.play();

	// var particles = this.add.particles('red');

	// var emitter = particles.createEmitter({
	// 		speed: 100,
	// 		scale: { start: 1, end: 0 },
	// 		blendMode: 'ADD'
	// });

	// emitter.startFollow(player);
}

function update() {
	if(addingNewImageForPlayer != undefined) {
		const image = this.add.sprite(addingNewImageForPlayer.position.x, addingNewImageForPlayer.position.y, 'ghost')
		image.setScale(0.15)
		gameState.playerData[addingNewImageForPlayer.token] = { image };

		if(localStorage.getItem('playerToken') == addingNewImageForPlayer.token) {
			player = image
		}

		addingNewImageForPlayer = undefined
	}
	
	if(addingNewImageForSnack != undefined) {
		const image = this.add.sprite(addingNewImageForSnack.x, addingNewImageForSnack.y, addingNewImageForSnack.image)
		image.setScale(0.15)
		gameState.snacksData[addingNewImageForSnack.token] = { image };

		addingNewImageForSnack = undefined
	}

	var cursors = this.input.keyboard.createCursorKeys();

	if (cursors.left.isDown) {
			player.x -= playMoveSpeed;
	} else if (cursors.right.isDown) {
			player.x += playMoveSpeed;
	}

	if (cursors.up.isDown) {
			player.y -= playMoveSpeed;
	} else if (cursors.down.isDown) {
			player.y += playMoveSpeed;
	}
}

function updateServer() {
	if(player != undefined) {
		socket.emit('updatePlayerInfo', {
			gameCode: localStorage.getItem("gameCode"),
			playerToken: localStorage.getItem("playerToken"),
			position: {x: player.x, y: player.y}
		})
	}
}